# Órdenes de compra

## Uso principal

Usar para:
- buscar órdenes de compra
- abrir detalle de OC
- revisar estado y acciones disponibles
- identificar XML, adjuntos, impresión y pagos
- preparar gestión sin ejecutar cambios no confirmados

## Rutas funcionales observadas

Desde el menú privado:
- `Orden de Compra -> Búsqueda y Gestión de Órdenes de Compra`
- `Orden de Compra -> Gestión de Órdenes de Compra`

## Filtros observados

- ID
- comprador
- rango de fechas
- estado
- sucursal

## Estados observados

- Nueva orden de compra
- En proceso
- Cancelación solicitada
- Aceptada
- Cancelada
- No aceptada
- Recepción conforme

## Acciones observadas según contexto de estado

- Aceptar
- Rechazar
- Solicitar cancelación
- Adjuntos
- Imprimir
- OC XML
- Ir a Mis Pagos

## Heurísticas

- Nunca aceptar/rechazar/cancelar sin confirmación explícita.
- Primero abrir detalle y resumir:
  - comprador
  - monto
  - estado actual
  - archivos disponibles
  - acciones visibles
- Si hay dashboard/gestión disponible, usarlo para priorizar pendientes antes de entrar una por una.

## Salidas útiles

- resumen de OC pendiente
- matriz de acciones posibles por estado
- advertencias antes de aceptar/rechazar
- siguiente paso sugerido
