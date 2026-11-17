# Activación de la suscripción y pago — powpow-register

## Conclusión (primero la respuesta)
> **Periodo de prueba gratuita (a partir del 2026-10-18; manda el comportamiento real de la plataforma)**: durante este periodo una cuenta registrada puede usar todas las funciones directamente, y **suscribirse es una mejora opcional, no un requisito** — sigue el flujo de este archivo solo cuando el usuario quiera activamente la membresía. Cuando el periodo de prueba termine, las cuentas sin suscripción que visiten páginas de contenido serán redirigidas a la página de suscripción; basta con completar la suscripción según este archivo.


**Tanto las suscripciones por Alipay como por PayPal las puede gestionar el agent: creación del pedido y seguimiento del cobro incluidos.**
Alipay es una compra única sin renovación automática, para usuarios de China continental y usuarios con Alipay; PayPal se renueva automáticamente cada mes y se puede cancelar en cualquier momento,
para usuarios en el extranjero y sin Alipay. El código QR de WeChat (confirmación manual) y Huawei IAP siguen existiendo, pero la habilidad no los gestiona.

Límites de responsabilidad en el pago: el agent puede **crear el pedido, abrir la caja y consultar el cobro**; **jamás** toca la cuenta Alipay/PayPal
del usuario ni sus credenciales de pago, y jamás promete «pagar por él». La acción de pagar la realiza siempre el propio usuario en la caja oficial.

## Canal de Alipay (vibepay, vía principal)

Compra única sin renovación: se paga una vez y se activa el periodo correspondiente, **sin renovación automática**. Los planes están fijados en
`src/lib/alipay-vibepay.ts` (`ALIPAY_PACKAGES`):

| key | planId | Nombre | Precio | Duración |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Membresía mensual | ¥6.99 | 30 días |
| `quarterly` | alipay-quarterly | Membresía trimestral | ¥19.99 | 90 días |
| `yearly` | alipay-yearly | Membresía anual | ¥69.99 | 365 días |

### Contrato de las interfaces (el script de la habilidad ya las encapsula, el agent no monta las peticiones a mano)

| Interfaz | Método | Descripción |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Requiere `Authorization: Bearer <JWT>` (basta un usuario pending). body `{package}` → devuelve `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` es una página de formulario que se autoenvía a la pasarela de Alipay |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Igualmente autenticación Bearer. Devuelve `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (callback del servidor de Alipay) | Verificación de firma en cinco puntos (firma, app_id, coincidencia de importe, TRADE_SUCCESS/TRADE_FINISHED, unicidad del comerciante) → actualización **idempotente** del pedido + creación de la suscripción + activación de la cuenta. La habilidad jamás toca esta interfaz |
| `/payment/alipay/return` | Página de retorno del navegador | Ruta pública; tras el pago muestra la confirmación de 「支付成功」 (pago completado) y sondea dentro de la página el estado real del backend |

- Los pedidos no pagados se **cierran automáticamente a las 2 horas**; si el usuario lo abandona a medias → vuelve a ejecutar `create-order` directamente, sin ocuparte del pedido viejo.
- El script escribe el `paymentHtml` en un archivo HTML temporal; el agent lo abre con un comando del sistema y ya se entra en la caja de Alipay
  (escaneando el código QR o iniciando sesión en Alipay para pagar).

### Cadena de activación (automática, sin intervención manual)

Verificación de firma del notify superada → `paymentOrders` marcado como pagado → `user_subscriptions` crea/prorroga
(`planId`, `currentPeriodEnd` calculados según durationDays; las renovaciones se prorrogan sobre la fecha de vencimiento original) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → la página de retorno sondea el paid y muestra el éxito.

## Tras el pago hay que renovar obligatoriamente el estado de sesión (importante)

El JWT lleva dentro la declaración de suscripción (en una cuenta pending es `NONE`). **El cobro del pago solo actualiza la base de datos, no modifica un
JWT ya emitido** — la declaración del token viejo sigue siendo NONE; si se usa directamente para generar el enlace de inicio de sesión, se manifestará como «sin membresía».
Por eso la habilidad, tras confirmar el `paid` / el `ACTIVE` de PayPal, ejecuta primero `refresh-login` (reinicia sesión y cambia por un JWT nuevo, con la declaración ACTIVE)
y después genera el enlace 2. Es comportamiento de diseño, no una corrección de bug.

## Canal de suscripción PayPal (lo gestiona la habilidad; web no HarmonyOS)

Solo hay un plan, Premium Monthly (unos $1/mes, según lo que devuelva `/api/subscription/plans`); **se renueva automáticamente cada mes**
y el usuario puede cancelarlo cuando quiera desde su cuenta de PayPal.

### Contrato de API (ya encapsulado por el script de la habilidad; el agent nunca arma las peticiones directamente)

| Endpoint | Método | Notas |
|---|---|---|
| `/api/subscription/plans` | GET | Auth Bearer; devuelve la lista de planes disponibles (ahora mismo solo 1) |
| `/api/subscription/create` | POST | Cuerpo `{planId}` → devuelve `{subscriptionId, approveUrl, status}`; `status` suele ser `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Auth Bearer; devuelve `{activeSubscription, allSubscriptions}`; el agente sondea `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | La llama automáticamente la página de éxito (con la cookie); activa directamente vía la API de PayPal si el webhook no ha llegado |
| `/subscription/success` | Página de retorno del navegador | Aterriza tras la autorización de PayPal; sondea verify automáticamente y vuelve al inicio / a la página original |
| `/subscription/cancel` | Página del navegador | Aterriza si el usuario cancela o algo falla; se puede reintentar |

### Flujo delegado

```
create-order --provider paypal  # → devuelve approveUrl, escrito en un archivo HTML local
abrir el archivo HTML           # → el navegador salta a la página de autorización de PayPal
query (cada 10–15 s)            # → sondear hasta ACTIVE
refresh-login                   # → cambiar a un JWT nuevo (declaración de suscripción ACTIVE)
login-link --target home        # → generar el enlace de inicio de sesión definitivo
```

- Las suscripciones PENDING que no se completan en 1 hora las limpia el backend automáticamente; basta con empezar de nuevo.
- Si el usuario repite `create-order`, el backend reutiliza la suscripción `APPROVAL_PENDING` aún válida, evitando un 409.
- Igual que con Alipay: el cobro solo actualiza la base de datos, el JWT viejo no se refresca solo, así que **hay que** ejecutar `refresh-login` antes de enviar el enlace al inicio.

## Los cuatro canales de la página de suscripción

La página de suscripción `src/app/(public)/subscription/page.tsx` muestra según el entorno de ejecución:

| Canal | Entorno | Mecanismo | Forma de activación |
|---|---|---|---|
| **Alipay (principal)** | Web | `AlipayPaymentSection` va por las interfaces de vibepay (tabla de arriba) | Activación automática del servidor vía notify, en segundos |
| Suscripción PayPal | Web (no HarmonyOS) | `/api/subscription/create` → salto a la autorización de PayPal; renovación mensual automática cancelable en cualquier momento (`/api/subscription/manage`) | El Webhook de PayPal (`BILLING.SUBSCRIPTION.*`) pone active automáticamente |
| Suscripción por código QR de WeChat | Web (no HarmonyOS) | Al pie de la página 「微信扫码订阅」 (escanea el código para suscribirte): transferencia por código QR | **Confirmación manual**, el cobro puede tardar en reflejarse; no concluyas con prisa que ha fallado justo después de pagar |
| Compra in-app de Huawei | Dentro de la app HarmonyOS | `NativeBridge.purchaseSubscription()` nativo | `/api/subscription/activate-huawei` valida el pedido de Huawei y activa |

Los planes y precios de PayPal se leen dinámicamente de `/api/subscription/plans`; texto fijo de la página: Auto-renews. Cancel anytime.

## Estados y saltos

- Alipay terminado → la página de retorno muestra el éxito; PayPal con éxito → `/subscription/success` → cuenta active →
  salto automático de vuelta a la página original indicada por el parámetro `next` (si no hay, al inicio).
- Un usuario ya suscrito que vuelva a la página de suscripción → ve "You're All Set!", y a los 3 segundos regresa automáticamente al inicio.
- Pago fallido / cancelado (PayPal) → `/subscription/cancel`, se puede volver a iniciar.

## Diagnóstico

| Síntoma | Gestión |
|---|---|
| Alipay terminado pero `query` sigue en pending | El notify rara vez se retrasa; espera 30 segundos y consulta de nuevo. Si sigue sin funcionar, que el usuario mire en el navegador el estado de la página de retorno; si aun así no, contacta con el soporte de la plataforma (dongtao@outlook.com) comunicando el `outTradeNo` |
| Alipay terminado, pero al entrar con el enlace 2 sigue bloqueado | Se saltó el `refresh-login` (la declaración del JWT viejo no se actualizó) — primero `refresh-login` y luego `login-link` |
| El `query` de PayPal sigue en PENDING | El usuario no ha terminado la autorización en PayPal; confirma que el enlace de autorización se abrió en el navegador. Si sigue PENDING tras autorizar, puede ser un retraso del webhook: pide al usuario que espere unos segundos más en la página de éxito o que la recargue |
| El `query` de PayPal devuelve 409 | Ya existe una suscripción PENDING sin terminar; espera 1 hora a que expire o completa la autorización del enlace antiguo en el navegador |
| PayPal pagado, pero al entrar con el enlace 2 sigue bloqueado | Igual que con Alipay: primero `refresh-login` y luego `login-link` |
| Tras pagar sigue 403 (PayPal) | El Webhook a veces se retrasa; reinicia sesión para refrescar el estado |
| Pagado por WeChat pero sin activación | La confirmación manual es asíncrona; si en unas horas no se activa, contacta con el soporte de la plataforma |
| La página de suscripción muestra "No subscription plans available" | `/api/subscription/plans` no tiene planes PayPal disponibles, problema de configuración del lado de la plataforma; los usuarios de China continental pueden irse por Alipay |

## Nota histórica

En el código existe además **una vieja** pasarela de pago web de Alipay (`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 compra única, degradada a pago simulado cuando el sandbox no tiene claves configuradas), que nunca se conectó a la UI de la página de suscripción y no tiene
relación con vibepay. La habilidad no la toca en ningún caso; `alipay-vibepay.ts` es el canal vigente.
