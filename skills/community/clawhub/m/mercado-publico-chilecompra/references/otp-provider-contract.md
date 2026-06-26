# Contrato conceptual `otp-provider`

## Propósito

Separar la lógica de negocio del login de Mercado Público de la tecnología específica usada para acceder al correo OTP.

El skill debe pensar en términos de:
- **necesito resolver un OTP**
- no en términos de:
- **necesito usar Himalaya / Gmail / Graph**

## Requisito previo

Antes de usar un `otp-provider`, el usuario debe haber definido:

1. el correo donde llegarán los OTP
2. el mecanismo concreto por el cual el agente accede a ese correo
3. que ese acceso ya fue validado funcionalmente

Si falta cualquiera de esos tres puntos, el flujo debe degradar a OTP manual.

## Interfaz conceptual mínima

Un `otp-provider` debe poder resolver estas preguntas:

### 1. `is_configured`
¿Existe una implementación configurada y usable para este usuario?

Salida esperada:
- `true` / `false`
- motivo si es `false`

### 2. `describe`
¿Qué canal/correo está usando para OTP?

Salida esperada:
- correo objetivo
- mecanismo de acceso (Himalaya / Google / Graph / otro)
- folder o fuente si aplica

### 3. `wait_for_otp`
Esperar OTP por una ventana acotada de tiempo.

Entradas mínimas:
- `target_email`
- `timeout_seconds`
- `context_started_at`
- filtros esperados (remitente/asunto)

Salida esperada:
- `status=found|timeout|error|manual_required`
- `otp` si existe
- metadatos mínimos útiles para diagnóstico

### 4. `validate_candidate`
Determinar si un correo candidato parece pertenecer al OTP del login actual.

Criterios típicos:
- remitente esperado
- asunto esperado
- recepción posterior al inicio del login
- patrón OTP válido

### 5. `explain_failure`
Explicar por qué no pudo resolver el OTP.

Ejemplos:
- acceso al correo no configurado
- inbox vacío en ventana de espera
- correo llegó pero no coincidió con filtros
- error del proveedor de correo
- se requiere fallback manual

## Contrato de comportamiento

Un `otp-provider` debe:
- evitar polling agresivo
- no persistir OTP en almacenamiento de largo plazo
- no exponer OTP completo en logs compartidos
- preferir el correo más reciente recibido después del inicio del login actual
- fallar de forma explícita y diagnóstica

## Resultado esperado por el skill

El skill de Mercado Público debería poder consumir un resultado como este, sin importar implementación:

```json
{
  "status": "found",
  "targetEmail": "otp@example.com",
  "provider": "external-mail-adapter",
  "receivedAt": "<ISO-8601 timestamp>",
  "otp": "ABC123"
}
```

O en fallo:

```json
{
  "status": "manual_required",
  "targetEmail": "otp@example.com",
  "provider": "unknown",
  "reason": "mail access not validated"
}
```

## Implementaciones posibles

Ejemplos de implementaciones que pueden cumplir este contrato:
- Himalaya
- Gmail / Google Workspace vía integración OpenClaw
- Microsoft Graph
- otra integración de lectura de correo

## Regla de diseño

La skill debe depender del **contrato** y no de una implementación específica.
La implementación concreta se elige por contexto del usuario.
