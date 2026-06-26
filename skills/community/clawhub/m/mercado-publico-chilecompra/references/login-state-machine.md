# Login/Auth state machine

## Objetivo

Estandarizar el flujo de autenticación en Mercado Público/ClaveÚnica para operar con seguridad, diagnosticar bloqueos y escalar a humano solo cuando corresponde.

## Estados y transiciones (vista rápida)

```text
not_authenticated
  -> credentials_entry
  -> manual_fallback_required

credentials_entry
  -> otp_requested
  -> error_state
  -> manual_fallback_required

otp_requested
  -> waiting_for_otp
  -> manual_fallback_required
  -> error_state

waiting_for_otp
  -> entity_selection
  -> otp_requested
  -> manual_fallback_required
  -> session_expired
  -> error_state

entity_selection
  -> authenticated
  -> session_expired
  -> manual_fallback_required
  -> error_state

authenticated
  -> session_expired
  -> manual_fallback_required
  -> error_state

session_expired
  -> credentials_entry
  -> manual_fallback_required

manual_fallback_required
  -> credentials_entry
  -> waiting_for_otp
  -> entity_selection
  -> authenticated
  -> error_state

error_state
  -> not_authenticated
  -> credentials_entry
  -> manual_fallback_required
```

## Estado por estado

### 1) `not_authenticated`

- **Gatilla cuando:** abrir portal y no existir sesión válida; detectar redirección al login público/ClaveÚnica.
- **Señales a observar:** ausencia de `Menu.aspx`; presencia de formulario de autenticación; retorno a home pública.
- **Acciones permitidas:** abrir flujo de login; verificar contexto (dominio, URL esperada, no iframe roto).
- **Transiciones válidas:** `credentials_entry`, `manual_fallback_required`.
- **Pedir intervención humana cuando:** exista bloqueo externo (CAPTCHA no automatizable, MFA fuera de correo esperado, bloqueo de cuenta).

### 2) `credentials_entry`

- **Gatilla cuando:** aparecer formulario ClaveÚnica para usuario/clave.
- **Señales a observar:** campos credenciales visibles; botón de continuar/login activo.
- **Acciones permitidas:** solicitar/usar método de ingreso autorizado; enviar credenciales por canal seguro definido por el usuario.
- **Transiciones válidas:** `otp_requested`, `error_state`, `manual_fallback_required`.
- **Pedir intervención humana cuando:** credenciales no disponibles, rechazo reiterado, o ClaveÚnica exige validación no soportada.

### 3) `otp_requested`

- **Gatilla cuando:** ClaveÚnica confirma credenciales y solicita OTP por correo.
- **Señales a observar:** pantalla/mensaje de “código enviado”; indicación de correo destino parcial.
- **Acciones permitidas:** iniciar ventana de espera OTP (hasta 5 min); buscar OTP con provider definido; preparar reintento.
- **Transiciones válidas:** `waiting_for_otp`, `manual_fallback_required`, `error_state`.
- **Pedir intervención humana cuando:** correo destino no coincide con el esperado, OTP nunca llega tras reintento razonable, o hay dudas de seguridad del código.

### 4) `waiting_for_otp`

- **Gatilla cuando:** OTP ya fue solicitado y está en curso la espera/lectura del código.
- **Señales a observar:** timer/contador en pantalla OTP; llegada de correo válido (remitente, asunto, timestamp y formato correcto).
- **Acciones permitidas:** extraer y enviar OTP; solicitar regeneración de OTP; reintentar búsqueda controlada.
- **Transiciones válidas:** `entity_selection`, `otp_requested`, `manual_fallback_required`, `session_expired`, `error_state`.
- **Pedir intervención humana cuando:** OTP caduca repetidamente, el usuario debe leer OTP manualmente, o hay discrepancia entre código detectado y pantalla.

### 5) `entity_selection`

- **Gatilla cuando:** autenticación exitosa y portal solicita seleccionar entidad/empresa.
- **Señales a observar:** selector de entidad visible; lista de empresas/unidades habilitadas.
- **Acciones permitidas:** listar opciones; confirmar entidad objetivo con el usuario; seleccionar entidad.
- **Transiciones válidas:** `authenticated`, `session_expired`, `manual_fallback_required`, `error_state`.
- **Pedir intervención humana cuando:** existen múltiples entidades ambiguas, falta criterio de selección, o aparece entidad inesperada.

### 6) `authenticated`

- **Gatilla cuando:** ingreso al shell proveedor (`Menu.aspx`) con contexto de entidad activo.
- **Señales a observar:** menú privado cargado; módulos internos accesibles; identidad/entidad visible.
- **Acciones permitidas:** navegación funcional; ejecutar runbooks de negocio; validar contexto antes de cada acción sensible.
- **Transiciones válidas:** `session_expired`, `manual_fallback_required`, `error_state`.
- **Pedir intervención humana cuando:** se requiera confirmación de acciones que cambian estado (ofertar, cotizar, aceptar/rechazar OC, reclamos).

### 7) `session_expired`

- **Gatilla cuando:** timeout, redirección a login, pérdida de contexto, o error por sesión inválida.
- **Señales a observar:** retorno a login/ClaveÚnica; módulos dejan de cargar; prompts de reautenticación.
- **Acciones permitidas:** informar expiración; reanudar desde login; preservar contexto de tarea para retomar.
- **Transiciones válidas:** `credentials_entry`, `manual_fallback_required`.
- **Pedir intervención humana cuando:** expiración ocurre en bucle o durante acción crítica sin confirmación de estado final.

### 8) `manual_fallback_required`

- **Gatilla cuando:** el flujo no puede continuar de forma confiable (OTP no resoluble, CAPTCHA, validación externa, ambigüedad crítica).
- **Señales a observar:** bloqueos repetidos; pantallas no automatizables; incertidumbre operativa.
- **Acciones permitidas:** pausar automatización; pedir paso humano concreto; documentar dónde retomar.
- **Transiciones válidas:** `credentials_entry`, `waiting_for_otp`, `entity_selection`, `authenticated`, `error_state`.
- **Pedir intervención humana cuando:** siempre (es un estado explícito de traspaso).

### 9) `error_state`

- **Gatilla cuando:** errores técnicos no recuperables en el paso actual (404 contextual, `NullReferenceException`, ruta quebrada, provider OTP fallando).
- **Señales a observar:** mensajes de error repetibles; stack/errores ASP.NET; ausencia de elementos esperados tras refresh controlado.
- **Acciones permitidas:** capturar evidencia mínima; clasificar causa probable; proponer ruta segura de recuperación.
- **Transiciones válidas:** `not_authenticated`, `credentials_entry`, `manual_fallback_required`.
- **Pedir intervención humana cuando:** haya riesgo de acción incorrecta o error persistente sin workaround seguro.

## Reglas transversales

- Validar estado antes de actuar; no asumir continuidad por URL.
- Reusar sesión válida; evitar reloguear por defecto.
- No exponer OTP completo en logs ni persistir secretos.
- Separar siempre: **leer → preparar → confirmar → ejecutar**.
- Detenerse ante ambigüedad de identidad, entidad o estado de sesión.
