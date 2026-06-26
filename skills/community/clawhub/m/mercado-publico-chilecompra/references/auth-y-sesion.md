# Auth y sesión

## Flujo base observado

1. Entrar a Mercado Público.
2. Redirección a ClaveÚnica.
3. Ingresar credenciales.
4. Ingresar OTP enviado por correo.
5. Seleccionar entidad/empresa.
6. Entrar al shell privado proveedor (`Menu.aspx`).

## Arquitectura recomendada (acceso genérico al correo)

Usar un esquema de correo **asignado al agente** para OTP:

1. El usuario define un buzón/cuenta para validaciones de ClaveÚnica (dedicado o controlado).
2. El usuario valida que el agente puede acceder a ese correo por un mecanismo confiable.
3. El usuario indica explícitamente cuál será ese correo.
4. En el login, cuando ClaveÚnica dispare OTP, el agente abre una ventana de espera de hasta 5 minutos.
5. El agente busca correo OTP por remitente/asunto y extrae código.
6. Usa el OTP inmediatamente (vigencia corta).

Implementaciones posibles:
- integración de OpenClaw con Google
- Microsoft Graph
- otra integración de lectura de correo elegida y validada por el usuario

Detalle operativo en:
- `references/acceso-a-correo-otp.md`
- `references/otp-provider-contract.md`

Nota:
- La versión pública de esta skill no empaqueta implementaciones concretas de lectura de inbox. El OTP automático, si se usa, debe resolverse mediante una integración externa elegida y autorizada por el usuario. Si no existe esa integración, usar fallback manual.

## Reglas operativas de sesión

- Reutilizar sesión activa si existe.
- No reloguear sin necesidad.
- Detectar selector de entidad y no asumir empresa única.
- Confirmar salida final en shell privado proveedor (no home pública).
- Si el broker de ClaveÚnica empieza a expirar, rechazar credenciales aparentemente válidas o perder contexto, preferir fallback manual del login y retomar desde la sesión ya autenticada.

## Señales de sesión válida

- Presencia de `Menu.aspx` o menú privado proveedor.
- Nombre de usuario visible.
- Empresa/unidad seleccionada visible.
- Módulos internos disponibles (Licitaciones, OC, Reclamos, Gestión, etc.).

## Señales de sesión inválida o vencida

- Redirección a login/ClaveÚnica.
- Retorno a home pública.
- Errores por falta de contexto al abrir módulos.
- Selector de entidad reaparece inesperadamente.

## Fallback si OTP no se puede resolver

1. Pedir al usuario regenerar código.
2. Reintentar escucha por otra ventana de hasta 5 minutos.
3. Si persiste, pasar a ingreso manual del OTP por el usuario.
4. Documentar causa probable (correo no llega, filtro antispam, cuenta/folder incorrecta, desfase de reloj).

## Guardrails mínimos

- No guardar credenciales de correo ni OTP en archivos de skill.
- No exponer OTP completo en logs compartidos.
- No cerrar sesión salvo instrucción explícita.
- Verificar remitente/asunto/contexto antes de usar cualquier código.
