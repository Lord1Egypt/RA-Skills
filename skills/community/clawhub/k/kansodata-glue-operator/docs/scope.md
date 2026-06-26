# Scope del Skill kansodata-glue-operator

## In-scope
- Diagnostico contractual de cambios en Glue para `workflows` y `triggers`.
- Planificacion atomica y reversible para `workflows` y `triggers`.
- Propuesta de cambio contractual (sin ejecutar) para `workflows` y `triggers`.
- Verificacion documental de evidencia posterior al cambio propuesto.

## Out-of-scope
- `jobs`
- `crawlers`
- secretos
- credenciales
- ejecucion de codigo
- ejecucion real AWS
- SDK runtime
- integracion con plugin
- nuevos plugins
- persistencia
- APIs externas

## Boundary decisions
- Si una solicitud mezcla `workflows/triggers` con `jobs/crawlers`, se rechaza completa (fail-closed).
- Si falta evidencia o credenciales, se degrada o rechaza segun riesgo, sin ejecutar.
- Si el rollback no esta definido para `apply-change`, se rechaza.

## Solicitudes aceptables
- "Diagnosticar drift de naming en trigger de un workflow declarado".
- "Plan-change para ajustar dependencia entre dos workflows".
- "Apply-change contractual para actualizar condicion de trigger sin ejecutar en AWS".
- "Verify de evidencia declarada posterior a cambio en trigger".

## Solicitudes rechazables
- "Modificar Glue Job y su script".
- "Crear o actualizar crawler de catalogo".
- "Ejecuta este cambio en AWS ahora".
- "Usa estas credenciales y aplica por SDK".
- "Sin rollback, aplica el ajuste".

## Decision especifica: workflows/triggers vs jobs/crawlers
- Permitido: cambios conceptuales y contractuales sobre `workflows` y `triggers`.
- Prohibido: cualquier analisis, plan o aplicacion sobre `jobs` y `crawlers`.
- Regla dura: presencia de `jobs` o `crawlers` activa rechazo inmediato.
