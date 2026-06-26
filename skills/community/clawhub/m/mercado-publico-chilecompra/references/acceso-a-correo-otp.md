# Acceso al correo para OTP (genérico)

## Objetivo

Resolver el OTP de ClaveÚnica sin depender necesariamente de ingreso manual del usuario.

## Prerequisitos del usuario

Antes de usar el login autenticado con OTP, el usuario debe garantizar:

1. que el agente **puede acceder** al correo donde llegarán los mensajes OTP
2. que el usuario **indique cuál será ese correo**
3. que el usuario **defina el mecanismo** por el cual el agente accederá a ese inbox
4. que el usuario **valide previamente** que ese acceso funciona en la práctica

Sin esas condiciones, el flujo debe degradar a OTP manual.

## Opciones válidas de acceso al correo

El skill debe tratar el acceso al correo de forma **genérica**. Algunas implementaciones posibles:

- integración de OpenClaw con Google Workspace / Gmail
- Microsoft Graph / Outlook / Exchange
- otro mecanismo confiable que permita al agente listar y leer correos recientes

La versión pública de esta skill no empaqueta un lector de inbox concreto. Cualquier automatización de OTP por correo debe resolverse mediante una integración externa, explícitamente elegida por el usuario y validada antes de usarla.

## Qué debe pedir la skill al usuario

Pedir explícitamente al usuario:

- qué correo se usará para recibir OTP de ClaveÚnica
- por qué mecanismo podrá acceder el agente a ese correo
- que valide antes que el agente realmente puede leer correos entrantes en ese buzón
- que confirme si desea OTP automático o fallback manual

Ver también:
- `references/otp-provider-contract.md`

## Flujo recomendado

1. Iniciar login ClaveÚnica.
2. Cuando el sitio avise que envió OTP, abrir ventana de espera de hasta 5 minutos.
3. Escuchar correos nuevos en el buzón indicado por el usuario.
4. Filtrar por remitente/asunto/contexto esperados.
5. Extraer el OTP.
6. Usarlo inmediatamente antes de expiración.
7. Si no llega, pedir regeneración o pasar a ingreso manual.

## Criterios prácticos base observados

- remitente esperado: `no-reply@digital.gob.cl`
- asunto esperado: contiene `ClaveÚnica - Código de validación de autenticación`
- vigencia: ~5 minutos
- OTP observado: alfanumérico en mayúsculas, 6 caracteres
- regex base útil: `\b[A-Z0-9]{6}\b`

## Guardrails

- no persistir OTP en memoria de largo plazo ni archivos
- no asumir que cualquier correo parecido sirve; validar remitente, asunto y timing
- si llegan varios correos, usar el más reciente recibido después del inicio del login actual
- si el acceso al correo no está confirmado, no prometer automatización completa del login
