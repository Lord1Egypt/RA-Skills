---
name: powpow-register
description: Ayuda a los usuarios a completar el registro de PowPow (Burbuja) y el inicio de sesión con un clic dentro de la conversación. El agent rellena el formulario en su nombre (incluida la subida de avatar) y envía el código de verificación por correo; el usuario solo aporta información básica y comprueba el código una vez, sin salir de la conversación. Durante el periodo actual de prueba gratuita de la plataforma, una cuenta registrada puede usar todas las funciones de inmediato; el pago de suscripción (Alipay/PayPal) es una mejora de membresía opcional, que el agent también puede gestionar con creación de pedidos y seguimiento del cobro cuando se necesite. Se activa cuando el usuario dice «registrarme en Burbuja», «crear una cuenta powpow», «cómo me registro en Burbuja», «ayúdame a crear una cuenta powpow», «sign up powpow»; también gestiona problemas de registro (código de verificación no recibido, nombre de usuario/correo ya ocupados) y problemas de activación (el login dice «cuenta no activada» / pending_payment, cómo suscribirse/pagar, ¿Burbuja es gratis o de pago?). Requiere Node ≥ 18; si no está disponible, vuelve automáticamente al modo de guía pura. No incluye publicar/crear humanos digitales (eso es cosa de powpow-simple) ni desarrollo de código.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (asistente de registro en Burbuja)

Lleva a un usuario nuevo desde «no sé qué es Burbuja» hasta «inicio de sesión con un clic, listo para jugar» — todo dentro de la conversación. El usuario solo sale de la conversación una vez: **para consultar el código de verificación en su correo**. La plataforma está actualmente en un periodo de prueba gratuita: una vez registrado, todas las funciones están disponibles, sin necesidad de pagar; el pago de suscripción es una mejora de membresía opcional (el agent también se encarga de abrir la caja y seguir el cobro).

**Versión 2.2.0** · 2026-10-18 (desde v2 este es el modo asistido por agent: el contrato del script y la secuencia completa están en `references/agent-flow.md`; las reglas de campos, los límites de tasa y la resolución de errores en `references/registration-flow.md`; los canales de pago en `references/payment-and-activation.md`; la lista de capturas de producto en `references/screenshots.md`. Desde v2.1.0 las suscripciones de PayPal también pueden ser gestionadas por el agent, como opción junto a Alipay. Desde v2.2.0 la plataforma entra en un periodo de prueba gratuita: regístrate y entra con un clic para empezar a usar; el pago pasa a ser una mejora opcional — si el usuario abre el enlace y aterriza en la página de suscripción, el periodo de prueba ha terminado, así que sigue el flujo de pago del Paso 7; el flujo se adapta solo, sin necesidad de cambiar el script)

## Entorno de ejecución

- Script principal `scripts/powpow-register.mjs`: **cero dependencias**, requiere **Node ≥ 18**. Antes de empezar, ejecuta una vez `node scripts/powpow-register.mjs status` para confirmar que el entorno funciona.
- Todas las peticiones del script van únicamente al dominio oficial `https://global.powpow.online`.
- **Sin Node / errores del script**: vuelve automáticamente al modo de guía pura — dale al usuario la página de registro https://global.powpow.online/register y acompáñalo según `references/registration-flow.md` (durante el periodo de prueba gratuita, el registro web es igual de inmediato). No insistas con el script.
- Reanudación tras una interrupción de la conversación: ejecuta primero `status` para ver en qué punto del flujo estás y continúa desde ahí.

## Trigger Conditions

- Intención de registro: «regístrate en Burbuja», «crear una cuenta de powpow», «cómo me registro en Burbuja», «sign up powpow»
- Registro atascado: «no me llega el código de verificación», «dice que el nombre de usuario ya existe», «la contraseña nunca pasa la validación»
- Problemas tras el registro: «el login dice que la cuenta no está activada», «403 pending_payment», «cómo pago/suscribo Burbuja», «¿Burbuja es gratis o de pago?»

**No se activa para**: publicar posts ni crear humanos digitales (→ powpow-simple); desarrollo de código del lado web (ver habilidades de desarrollo). Si el usuario quiere registrarse y también publicar: completa primero esta habilidad y, tras la activación, pásalo a powpow-simple.

## Resumen del flujo

| Paso | Qué hace el agent | Qué hace el usuario |
|---|---|---|
| 1 Presentación del producto | Presenta + envía capturas | Echa un vistazo |
| 2 Confirmación de datos | Sugiere nombre de usuario/apodo, contraseña con dos opciones, pide el correo | Confirma, proporciona |
| 3 Envío del código | `send-code` | —— |
| 4 Lectura del código | —— | Va al correo, busca el código de 6 dígitos y lo envía de vuelta |
| 5 Envío del registro | `register` (con subida directa del avatar), gestiona errores automáticamente | —— |
| 6 Inicio de sesión con un clic | `login-link(home)` directo a la página de inicio; si aterriza en la página de suscripción, ve al Paso 7 | Haz clic en el enlace y empieza a jugar |
| 7 Mejora de suscripción (opcional) | Solo cuando el usuario quiere membresía / el periodo gratuito ha terminado: flujo de pago completo gestionado | Elige un método, paga |
| 8 Cierre | `cleanup` + entrega de credenciales + guía de uso + recomendación de plugins | Empieza a jugar |

## Paso 1: presentación del producto + capturas (no se puede saltar)

La mayoría de los usuarios nunca ha visto Burbuja. Lo primero no es explicar el flujo, sino hacer que **vea** el producto:

1. Presenta Burbuja en ~120 caracteres: convierte las fotos tomadas al vuelo en un diario de viaje, clavado en el mapa público como una «burbuja»; las burbujas pierden vigencia con el tiempo y los «me gusta» de otros pueden revivirlas; en el mapa también hay «humanos digitales» con los que se puede conversar. Dirección de la plataforma: https://global.powpow.online ; si quiere ver primero un vídeo: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Envía capturas**. Las capturas ya viajan con la habilidad en `assets/screenshots/powpow-0N.jpg` — envíalas directamente como archivos locales, sin necesidad de conexión. El inventario, el contenido de cada imagen y cuándo usarlas están en `references/screenshots.md`. La combinación más habitual al abrir: página del mapa (powpow-03) + página de detalle de un post (powpow-06).

Reglas de capturas (reglas firmes):

- Las capturas **ya van incluidas con la habilidad** en `assets/screenshots/` (`powpow-0N.jpg`) — envíalas directamente como archivos de imagen locales; sirven en cualquier entorno, incluidos aquellos donde GitHub no abre.
- Envía solo 1–3 imágenes relacionadas con el tema actual, no las pegues todas de golpe.
- Si por accidente faltan archivos del paquete, recurre a los enlaces hospedados listados en `references/screenshots.md` (ojo: puede que no abran en China continental).

Al terminar la presentación, deja la decisión en manos del usuario: **«Si quieres registrarte, en tres minutos dejamos la cuenta creada aquí en la conversación; solo tendrás que mirar una vez el código que llega a tu correo.»**

## Paso 2: confirmar los datos de registro (una pregunta por turno, no las preguntes todas de golpe)

- **Nombre de usuario** (obligatorio): **sugiere proactivamente uno** a partir del contexto de la conversación o del nombre de usuario del sistema (2~50 caracteres, sin distinguir mayúsculas de minúsculas); si el usuario asiente, se usa; si quiere cambiarlo, se cambia.
- **Contraseña** (obligatoria; primero ofrece dos opciones):
  - El usuario la proporciona → luego se pasa al script mediante una variable de entorno, **nunca como argumento de la línea de comandos**;
  - La genera el agent → ejecuta `node scripts/powpow-register.mjs gen-password` y **envía de inmediato la contraseña generada al usuario para que la guarde** (se muestra solo esta vez y no vuelve a aparecer).
- **Correo electrónico** (obligatorio): debe proporcionarlo el usuario — es el ancla de identidad de la cuenta, **no lo adivines por él**.
- **Apodo** (opcional): sugiere que por defecto coincida con el nombre de usuario.
- **Avatar** (opcional): si el usuario da la ruta de una imagen local (≤5 MB, no SVG), el script la sube directamente; si no, se omite (la plataforma usa el logo por defecto); si tienes capacidad de generar imágenes, puedes ofrecerte a crearle una.
- **Teléfono** (opcional, número de China continental): omítelo por defecto; pídelo solo si el usuario quiere vincularlo.

Una vez confirmado, puedes ejecutar `prepare-suggest --username U --nickname N --email E` para dejarlo anotado en el archivo de estado (así register no vuelve a pedirlo).

## Pasos 3–4: código de verificación por correo (la única parte que exige salir de la conversación)

```
node scripts/powpow-register.mjs send-code --email <correo>
```

Después dile claramente al usuario: **ve al correo y busca el código de verificación de 6 dígitos, válido durante 10 minutos; acuérdate de mirar también la carpeta de spam o correo publicitario**; cuando lo encuentre, que vuelva y te lo envíe. El envío tiene una espera de 60 segundos, no lo repitas en cadena.

## Paso 5: enviar el registro (gestión delegada en el agent)

```
POWPOW_REGISTER_PASSWORD=<contraseña> node scripts/powpow-register.mjs register --code <código> [--username U] [--nickname N] [--avatar <ruta de imagen local>] [--phone P]
```

Si tiene éxito, la cuenta queda creada (estado pending, con 3 insignias iniciales). Los errores habituales se gestionan automáticamente, sin interrumpir al usuario:

| Error | Gestión |
|---|---|
| 「用户名已存在」(el nombre de usuario ya existe) | Sugiere automáticamente una variante (nombre de usuario + número) y, cuando el usuario la confirma, reintenta directamente (el código sigue siendo válido, no hace falta reenviarlo) |
| 「邮箱已被使用」(el correo ya está en uso) | Pregunta al usuario: ¿cambias de correo, o en realidad ya tienes cuenta? (pásalo a inicio de sesión / recuperación de contraseña) |
| 「邮箱验证码错误或已过期」(código de verificación incorrecto o caducado) | Si pasaron más de 10 minutos → volver a `send-code` |
| Envío/registro demasiado frecuentes (429) | Espera 1 minuto y reintenta; basta con avisar al usuario |

## Paso 6: Inicio de sesión con un clic (directo a la página de inicio tras el registro)

1. Justo después de registrarte con éxito:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Envía el enlace al usuario: **ábrelo y aterrizarás directamente en la página de inicio, ya con la sesión iniciada**. La plataforma está actualmente en un periodo de prueba gratuita: tras registrarte, todas las funciones están disponibles (feed, mapa, humanos digitales, check-ins, etc.), **sin necesidad de pagar**.
3. Pide al usuario que confirme si ha entrado; hay dos casos:
   - **Aterrizó en la página de inicio** → pasa directamente al Paso 8 para cerrar; el registro está completo;
   - **Aterrizó en la página de suscripción** → el periodo de prueba gratuita de la plataforma ha terminado; dile al usuario «el periodo de prueba gratuito ha terminado, ahora se requiere una suscripción de membresía», luego sigue el Paso 7 para completar la suscripción y vuelve al Paso 8 cuando termines.
4. Si el usuario quiere activamente mejorar o apoyar la plataforma → ve también al Paso 7 (suscribirse es voluntario; no insistas).
## Paso 7: Mejora de suscripción (opcional — solo cuando el Paso 6 lo requiera)

1. Primero envía el enlace de semi-sesión para que la página de retorno del pago muestre correctamente «Pago realizado»:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Envía el enlace al usuario: al abrirlo, el navegador aterriza directamente en la página de suscripción, ya con la sesión iniciada.
2. **Deja que el usuario elija el método de pago** — muestra ambos canales:
   - **Alipay (China continental / usuarios con Alipay)**: compra única de la duración correspondiente, **sin renovación automática**
     - Mensual **¥6.99** (recomendado para probar) / Trimestral **¥19.99** / Anual **¥69.99**
   - **PayPal (ultramar / usuarios sin Alipay)**: se renueva mensualmente, cancela cuando quieras
     - Premium Monthly, unos **$1/mes** (según lo mostrado en la página de suscripción; renovación automática)
3. Una vez que el usuario elige:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   El script devuelve la ruta del archivo de la página de pago; **ábrelo directamente con un comando del sistema** (Windows: `start <archivo>`; macOS: `open <archivo>`; Linux: `xdg-open <archivo>`). El navegador saltará automáticamente a la caja oficial de Alipay/PayPal, donde el usuario completa el pago o la autorización de facturación.
4. Ejecuta `query` cada 10–15 segundos hasta que devuelva `paid` o `ACTIVE` (el cobro/autorización suele llegar en unos segundos o un minuto). Si el usuario cierra la página de pago a mitad → vuelve a ejecutar `create-order` directamente (los pedidos antiguos / suscripciones pendientes se cierran o caducan automáticamente tras 2 horas; ignóralos).
5. El canal de código QR de WeChat se confirma manualmente y el cobro puede tardar; Huawei IAP solo está disponible dentro de la app HarmonyOS. El skill no gestiona esos dos — tras pagar, el usuario vuelve y lo cuenta, y el agent ejecuta primero `whoami` para confirmar el cobro y luego envía el enlace a la página de inicio del punto 6 siguiente.
6. Tras confirmar el cobro, cambia a un estado de sesión con la declaración de suscripción más reciente y envía el enlace directo a la página de inicio:
   ```
   POWPOW_REGISTER_PASSWORD=<contraseña> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Envía el enlace al usuario: **ábrelo y aterrizarás directamente en la página de inicio con la membresía completa**.
## Paso 8: Cierre

1. `node scripts/powpow-register.mjs cleanup` para limpiar los archivos de estado temporales locales (credenciales de sesión).
2. Dale al usuario una «ficha de cuenta»: nombre de usuario, correo (la contraseña no se muestra de nuevo — en el modo generado ya se pidió al usuario que la guardara al generarla; si el usuario la puso él mismo, él la sabe).
3. Recordatorio de membresía (dilo una vez, no insistas): actualmente es un periodo de prueba gratuita y la cuenta se puede usar de inmediato; cuando el periodo de prueba termine, las cuentas sin suscripción que visiten páginas de contenido serán redirigidas a la página de suscripción — para un uso prolongado, vuelve y pide al agent que te suscriba cuando quieras.
4. Guía los primeros pasos: mirar el mapa, publicar el primer diario de viaje (→ pasa a powpow-simple).
5. Recomienda extensiones: el skill `@durenzidu/powpow-integration` y el plugin `@durenzidu/openclaw-channel-powpow` — conecta Burbuja con el agent del propio usuario; da el comando de instalación si lo quiere.
6. Cierra con un bloque de «siguiente paso».
## Conversation UX

Mantén el tono de servicio habitual de powpow:

- **El usuario es el sujeto de la frase**; «puedes…» es mejor que «necesito que…»; nada de sermones ni tono condescendiente.
- **Cada turno avanza una sola decisión**; antes de pedir un dato, da la razón.
- **Al final de cada respuesta** va un bloque fijo de «siguiente paso» (separador + 👉 + una única acción + una frase de «cuando lo hagas, yo…»), por ejemplo:
  ```
  ────────────────────
  👉 Ahora te toca: ve al correo, busca el código de 6 dígitos y envíamelo directamente
     (en cuanto lo reciba, creo la cuenta)
  ```
- **No sueltes sermones de seguridad sobre la contraseña**; no expliques mecanismos internos, límites de frecuencia ni diseño de seguridad, salvo que el usuario pregunte.
- Cuando el agent gestione tareas, informa todavía más del progreso: tras cada paso de script, di en una frase qué acaba de pasar («la cuenta ya está creada», «ya te abrí la página de pago»).

## Reglas firmes

- **Seguridad de las credenciales**: la contraseña se pasa al script solo mediante la variable de entorno `POWPOW_REGISTER_PASSWORD`, **nunca** como argumento de la línea de comandos (visible en la lista de procesos) ni escrita en ningún archivo (en modo generación se muestra una vez para que el usuario la guarde y no se vuelve a repetir). El código de verificación solo se usa en la interfaz oficial de registro y se descarta tras usarse.
- **Límite oficial**: todas las peticiones van únicamente a `https://global.powpow.online` (ya integrado en el script); jamás envíes información del usuario a direcciones de terceros.
- **Límite de pago**: el agent solo crea el pedido, abre la caja y consulta el cobro; **jamás** toca la cuenta Alipay/PayPal del usuario ni sus credenciales de pago, y jamás promete «pagar por él».
- **El muro de pago no es un bug**: durante el periodo actual de prueba gratuita todas las páginas de contenido están abiertas; si el usuario abre el enlace a la página de inicio pero aterriza en la página de suscripción, el periodo de prueba ha terminado — guíalo a suscribirse mediante el Paso 7. No intentes saltarte el muro de pago ni expliques mecanismos internos al usuario.
- **Libertad de retroceso**: si en cualquier paso el usuario quiere hacerlo por sí mismo, o el entorno no soporta el script, retrocede en cualquier momento al modo de guía pura — da los enlaces, explica las reglas y acompaña en la resolución de errores.
- No inventes reglas de la plataforma: las reglas de campos, los textos de error y los parámetros de límite provienen del código de la plataforma (`references/registration-flow.md` cita las fuentes); si la plataforma se actualiza, manda el comportamiento real.
- Para mostrar imágenes usa solo las capturas incluidas en `assets/screenshots/` (el uso de cada una está en `references/screenshots.md`).
- Cierra cada turno con el bloque de «siguiente paso», para que el usuario sepa siempre qué le toca hacer ahora.
