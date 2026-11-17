# Detalle del flujo de registro — powpow-register

Para consultarlo al diagnosticar problemas. Todas las reglas provienen del código fuente de la plataforma (validación consistente frontend/backend en Next.js), con la fuente citada.
Si la plataforma se actualiza, manda el comportamiento real en línea.

## Puntos de entrada

- Página de registro: https://global.powpow.online/register
- Página de inicio de sesión: https://global.powpow.online/login
- Página de suscripción: https://global.powpow.online/subscription
- Si se entra desde un enlace compartido con `?next=...`, al terminar registro + pago se salta automáticamente de vuelta a la página original.

## Campos del formulario y reglas

| Campo | Obligatorio | Regla | Fuente en el código |
|---|---|---|---|
| Avatar | Opcional | Imagen ≤5MB, sin soporte de SVG; el servidor comprime automáticamente (>100KB se comprime a 400×400 / calidad 90) | `src/app/api/auth/register/route.ts` |
| Nombre de usuario | Obligatorio | 2~50 caracteres, tras trim se almacena en **minúsculas** (Tom y tom cuentan como el mismo nombre de usuario; tanto el registro como el inicio de sesión son insensibles a mayúsculas/minúsculas) | Ídem (zod schema) |
| Contraseña | Obligatoria | 8~100 caracteres, debe incluir a la vez letra mayúscula, letra minúscula y número | Ídem |
| Confirmar contraseña | Obligatoria | Coincidir con la contraseña (solo validación del frontend) | `src/app/(public)/register/page.tsx` |
| Apodo | Opcional | ≤100 caracteres; si se deja vacío se toma por defecto el nombre de usuario | register route |
| Correo | **Obligatorio** | Formato de correo válido, ≤255 caracteres; un correo solo puede registrarse en una cuenta | register route |
| Código de verificación por correo | **Obligatorio** | 6 dígitos; **válido 10 minutos**; al validarse con éxito queda anulado; un reenvío marca el código viejo como usado | `src/lib/email-verification.ts` |
| Teléfono | Opcional | Número de China continental, 11 dígitos empezando por `1[3-9]`; un número de teléfono solo puede vincularse a una cuenta | register route |

La página ofrece además tres botones de inicio de sesión con terceros: **Google, Watcha, cuenta Huawei** (`GoogleSignInButton` /
`WatchaLoginButton` / `HuaweiLoginButton`). Las cuentas de terceros no tienen contraseña local; al intentar iniciar sesión después con contraseña se
obtiene 「该账号未设置密码，请使用其他方式登录」 (esta cuenta no tiene contraseña configurada, inicia sesión con otro método).

## Parámetros de límite de frecuencia y anti-fuerza bruta

| Acción | Límite | Fuente |
|---|---|---|
| Envío de registro | **3 veces/minuto/IP**, pasarse da 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Envío del código de verificación | Mismo IP 1 vez/minuto **y** mismo correo 1 vez/minuto, pasarse da 429; el botón del frontend tiene cuenta atrás de 60 segundos | `src/app/api/auth/register/send-code/route.ts` |
| Validación del código | Por correo, como máximo **5 intentos** en 10 minutos; alcanzado el límite se rechaza aunque el código sea correcto; hay que pedir uno nuevo | `src/lib/email-verification.ts` |
| Código de recuperación de contraseña | 1 vez/minuto/IP | `src/app/api/auth/forgot-password/route.ts` |
| Inicio de sesión | 5 veces/minuto/IP; la misma cuenta con **5 fallos** consecutivos queda **bloqueada 30 minutos** (423), con aviso de intentos restantes decreciente durante el bloqueo | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Comportamiento de protección de privacidad**: al enviar el código de verificación / la recuperación de contraseña, si el correo ya está registrado o no existe, la interfaz devuelve en ambos casos un
mensaje de éxito uniforme, sin revelar si el correo está registrado o no.

## Equivalencia entre el modo de gestión delegada del agent y el registro web

El script de la habilidad llama a **el mismo conjunto de API públicas** (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`), y recorre exactamente las mismas validaciones, límites de frecuencia y rutas de error que el envío del formulario de la página de registro — todas las
reglas de este archivo se aplican por igual a ambos modos. La secuencia del script y el contrato de comandos están en `references/agent-flow.md`.

## Flujo de estado tras el registro exitoso

> **Periodo de prueba gratuita (a partir del 2026-10-18; manda el comportamiento real de la plataforma)**: una cuenta recién registrada puede **usar todas las funciones directamente**
> (feed, mapa, humanos digitales, check-ins, etc.) sin necesidad de pagar; las cuentas sin suscripción ya no son bloqueadas en las páginas de contenido. La descripción del
> «bloqueo pending» de esta sección es el estado normal tras el fin del periodo de prueba — cuando llegue ese momento, manda el comportamiento real en línea.

1. El usuario se guarda con `accountStatus: 'pending'` y **3 insignias iniciales** (register route).
2. El servidor planta además dos cookies HttpOnly: el JWT (puede acceder a las páginas directamente) y
   el pendingUserToken (credencial de identidad para el flujo de suscripción).
3. En el estado normal (periodo de prueba terminado / sin periodo gratuito), la página de registro detecta `pending_payment` → redirige a `/subscription`
   (conservando el parámetro de retorno `next`); en el modo asistido por agent, `me?token=…&redirect=/subscription` consigue el mismo efecto.
   **Durante el periodo de prueba gratuita este paso no se dispara** — tras registrarte, entra directamente a la página de inicio y empieza a usar.
4. Pago completado → `accountStatus` pasa a `active` (**Alipay activa automáticamente en el servidor vía notify**;
   PayPal activa vía Webhook; el código QR de WeChat se confirma manualmente; Huawei IAP pasa por `activate-huawei`).
   Ver detalles en `payment-and-activation.md`.

En el estado normal, los usuarios inactivos (pending) que llamen a las API núcleo (feed, mapa, chat de humanos digitales, check-ins, etc.) reciben 403;
los enlaces de posts compartidos son la excepción (se mantienen accesibles públicamente). Durante el periodo de prueba gratuita este bloqueo queda suspendido y todo está abierto.
## Tabla de diagnóstico de errores frecuentes

| Síntoma | Causa | Qué hacer |
|---|---|---|
| 「用户名已存在」 (el nombre de usuario ya existe) | Nombre de usuario ocupado (sin distinguir mayúsculas/minúsculas) | Probar otro nombre de usuario |
| 「邮箱已被使用」 (el correo ya está en uso) | El correo ya se registró antes | Cambiar de correo; o pasar por inicio de sesión +「忘记密码」(olvidé mi contraseña) para recuperar la cuenta vieja |
| 「邮箱验证码错误或已过期」 (código de verificación incorrecto o caducado) | Código mal escrito / pasados los 10 minutos / rechazado por superar los 5 intentos fallidos | Pulsar 「重新发送」(reenviar) y usar el código del **correo más reciente** |
| No llega el código de verificación | Límite de 60 segundos; o cayó en spam / correo publicitario | Esperar a que acabe la cuenta atrás y reenviar; revisar la carpeta de spam |
| 「手机号已被使用」 (el teléfono ya está en uso) | El número ya está vinculado a otra cuenta | Quitar el teléfono (es opcional) o cambiar de número |
| 「注册请求过于频繁」 (solicitud de registro demasiado frecuente) / 429 | Techo de 3 registros/minuto/IP alcanzado | Esperar unos minutos y reintentar |
| 409 「用户名或邮箱已被注册」 (nombre de usuario o correo ya registrado) | Choque de nombre con otra persona en el instante del envío (red de seguridad ante concurrencia) | Cambiar nombre de usuario o correo y reintentar |
| 「图片大小不能超过5MB」 (la imagen no puede superar 5MB) / 「不支持 SVG」 (SVG no soportado) | Avatar fuera de norma | Cambiar de imagen o saltarse el avatar |
| El usuario abre el enlace de login pero aterriza en la página de suscripción (en vez de la de inicio) | El periodo de prueba gratuita ha terminado y el muro de pago de la plataforma ha vuelto | Sigue el flujo de pago por suscripción del Paso 7 de SKILL.md; tras suscribirte, ejecuta `refresh-login` y luego envía el enlace a la página de inicio |
| Registrado con éxito pero el login devuelve 403 «请完成订阅以激活账户» | La cuenta sigue pending, y la plataforma no está en un periodo de prueba gratuita (estado esperado antes de pagar) | No ocurre durante el periodo de prueba gratuita; si ocurre, el periodo de prueba ha terminado — completa primero la suscripción; si sigue dando 403 tras pagar, se usó un JWT antiguo — en el modo script ejecuta primero `refresh-login` para cambiar a un nuevo estado de sesión |
| Inicio de sesión 423 「账户已锁定」 (cuenta bloqueada) | 5 fallos seguidos de contraseña | Esperar 30 minutos |
| Inicio de sesión 401 「还剩 N 次尝试机会」 (te quedan N intentos) | Contraseña errónea, cerca del bloqueo | Pensarlo bien antes de reintentar, o ir directamente a 「忘记密码」(olvidé mi contraseña) |
| 「该账号未设置密码，请使用其他方式登录」 (esta cuenta no tiene contraseña configurada, inicia sesión con otro método) | Cuenta de tercero (Google/Watcha/Huawei) | Iniciar sesión con el botón de terceros original |
| 「该账号已注销」 (esta cuenta ha sido dada de baja) | La cuenta está desactivada | Hay que registrarse de nuevo |

## Nociones de inicio de sesión (útiles de paso para diagnosticar)

El inicio de sesión admite entrada triple **nombre de usuario / correo / teléfono** (cualquiera de los tres sirve como nombre de cuenta).
Contraseña olvidada: página de inicio de sesión → 「忘记密码」(olvidé mi contraseña) → introducir el correo de registro para recibir un código de 6 dígitos → restablecer.
