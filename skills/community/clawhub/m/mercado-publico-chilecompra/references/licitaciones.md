# Licitaciones

## Uso principal

Usar para:
- buscar licitaciones para ofertar
- abrir ficha de una licitación
- revisar preguntas y respuestas
- revisar adjuntos, bases, etapas y criterios
- diagnosticar por qué no se puede ofertar

## Ruta funcional base

Desde el menú privado:
- `Licitaciones -> Búsqueda de Licitaciones para Ofertar`

## Capacidades observadas

- búsqueda por ID
- búsqueda avanzada por nombre
- filtros por fecha de publicación o cierre
- filtros por región, estado y organización
- vistas para:
  - licitaciones de mis rubros
  - licitaciones ofertadas
  - licitaciones seguidas
- acceso a ficha de detalle
- acceso a preguntas
- descarga de información/adjuntos según proceso

## Estado y prerequisitos

Se observó un aviso importante:
- para ofertar se requiere proveedor en **estado hábil** en el Registro de Proveedores

## Heurísticas

- Si `Ofertar` está deshabilitado, explicar primero la causa probable:
  - proveedor no hábil
  - proceso no vigente
  - modalidad o etapa no compatible
  - restricción por permisos/contexto
- Antes de preparar una oferta, revisar:
  - estado del proceso
  - fecha de cierre
  - preguntas abiertas
  - adjuntos y bases
  - evidencia de que el botón de acción está realmente habilitado

## Salidas útiles para el usuario

- resumen ejecutivo de la licitación
- checklist de revisión
- riesgos visibles
- acciones disponibles ahora
- próximos pasos seguros
