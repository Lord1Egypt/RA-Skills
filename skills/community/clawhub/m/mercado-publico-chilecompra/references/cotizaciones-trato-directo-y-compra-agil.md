# Cotizaciones, trato directo y compra ágil

## Uso principal

Usar para:
- revisar invitaciones o solicitudes de cotización
- preparar una respuesta sin enviarla aún
- revisar módulos de trato directo o compra ágil
- detectar si una acción está habilitada o si el módulo está roto

## Cotizaciones

### Capacidades observadas
- búsqueda de cotizaciones
- apertura de detalle/respuesta
- revisión de ítems
- revisión de precios, impuestos, despacho, vigencia y adjuntos
- presencia de botón de envío final

### Regla
- Completar o revisar hasta el punto previo a `Enviar Cotización`, pero no enviar sin confirmación explícita.

## Trato Directo

### Observado
- listado y detalle funcionales
- presencia de acciones del tipo “ingresar solicitud”

### Regla
- permitir navegación y preparación
- no ejecutar envío definitivo sin confirmación

## Compra Ágil

### Observado
- módulo accesible con filtros/listados
- sensible a validaciones y formato de fecha

### Regla
- validar entradas con cuidado
- explicar errores de formato en vez de insistir ciegamente

## Invitaciones a servicios especializados

- revisar si existen invitaciones activas
- si no hay resultados, informar claramente que no se observan invitaciones para la cuenta actual

## Heurísticas comunes

- si el módulo abre pero falla al enviar, distinguir entre:
  - error del portal
  - dato inválido
  - requisito faltante
  - bloqueo por contexto/sesión
