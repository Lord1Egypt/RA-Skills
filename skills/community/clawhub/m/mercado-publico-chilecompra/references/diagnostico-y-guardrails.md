# Diagnóstico y guardrails

## Errores frecuentes a reconocer

### 404
Posibles causas:
- URL abierta fuera de contexto
- ruta legacy rota
- módulo ya no expuesto por acceso directo
- dependencia de iframe o postback

### Error .NET / `NullReferenceException`
Posibles causas:
- bug real del portal
- estado interno incompleto
- entrada directa sin precondiciones
- sesión parcialmente inválida

### Botón deshabilitado
Posibles causas:
- proveedor no hábil
- etapa no disponible
- fecha vencida
- rol insuficiente
- prerrequisito faltante

### Redirección inesperada
Posibles causas:
- sesión vencida
- módulo externalizado
- transición a centro de ayuda
- flujo nuevo fuera del shell legacy

### CAPTCHA / validación externa
Posibles causas:
- protección anti-bot
- formulario expuesto en módulo moderno

## Respuesta recomendada ante fallos

Siempre devolver:
1. qué pasó
2. causa probable
3. si parece problema del usuario o del portal
4. siguiente paso seguro

## Guardrails obligatorios

Pedir confirmación explícita antes de:
- ofertar
- enviar cotización
- aceptar OC
- rechazar OC
- solicitar cancelación
- enviar reclamo
- cambiar cualquier estado operativo/comercial

## Regla práctica

Primero:
- leer
- resumir
- preparar

Solo después:
- confirmar
- ejecutar

Si el estado del portal es ambiguo, detenerse y explicarlo en vez de “probar suerte”.
