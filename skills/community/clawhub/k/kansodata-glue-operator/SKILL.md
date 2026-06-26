# SKILL: kansodata-glue-operator

## Proposito
Definir un contrato operativo endurecido para gestionar cambios conceptuales en AWS Glue sin ejecucion real.
El skill opera solo a nivel de analisis, planificacion, propuesta y verificacion contractual.

## Modos operativos soportados
- `diagnose`
- `plan-change`
- `apply-change`
- `verify`

## Flujo operativo obligatorio
`read -> diagnose -> plan -> validate -> apply -> verify`

## Inputs aceptados
- `mode`: uno de los modos soportados.
- `request_id`: identificador de trazabilidad.
- `target`: recurso objetivo declarado.
- `scope`: debe limitarse a `workflows` y/o `triggers`.
- `current_state`: estado conocido, evidencia o inventario disponible.
- `constraints`: restricciones operativas y de seguridad.
- `acceptance_criteria`: criterios verificables de salida.
- `rollback_plan`: obligatorio para `apply-change`.

## Outputs esperados
Salida estructurada con:
- `mode`
- `status` (`ok`, `degraded`, `rejected`)
- `summary`
- `in_scope_actions`
- `out_of_scope_detected`
- `validation`
- `rollback`
- `evidence`
- `next_step`

## Contrato por modo
### `diagnose`
- Evalua input, riesgos y desalineaciones.
- No genera acciones aplicadas.
- Puede devolver `degraded` por falta de credenciales o evidencia.

### `plan-change`
- Genera plan atomico y reversible.
- Debe mapear cada accion a criterio de aceptacion.
- Debe incluir validaciones pre y post.

### `apply-change`
- Produce propuesta de cambio contractual, no ejecucion real.
- Permite solo acciones orientadas a `workflows` y `triggers`.
- Requiere `rollback_plan` explicito y validado.

### `verify`
- Contrasta evidencia contra criterios esperados.
- Informa cumplimiento, brechas y riesgo residual.
- No inventa evidencia faltante.

## Restricciones obligatorias
- Solo superficie de escritura conceptual: `workflows` y `triggers`.
- Prohibido modificar o proponer cambios sobre `jobs` y `crawlers`.
- Prohibidos secretos y credenciales.
- Prohibida ejecucion de codigo y ejecucion real AWS.
- Prohibido usar SDK runtime.
- Prohibida persistencia y APIs externas.
- Prohibida integracion con plugin.
- Prohibido afirmar acciones no ejecutadas.

## Guardrails
- Fail-closed por defecto.
- Alcance minimo necesario.
- Rechazo ante ambiguedad critica.
- Validacion previa obligatoria antes de `apply-change`.
- Verificacion posterior obligatoria para cierre.

## Fuera de alcance
- Runtime operativo real.
- Automatizacion de despliegues.
- Administracion de secretos.
- Acciones sobre recursos fuera de `workflows` y `triggers`.

## Degradacion segura
Si no hay credenciales AWS o acceso de lectura confiable:
- operar en modo contractual,
- marcar `status: degraded`,
- detallar limitaciones,
- entregar diagnostico/plan/verificacion parcial segun evidencia disponible,
- no simular ejecucion.

## Casos de rechazo
`status: rejected` cuando:
- el modo no es valido,
- el scope incluye `jobs` o `crawlers`,
- se solicita ejecucion real,
- se solicitan secretos/credenciales,
- no hay rollback para `apply-change`,
- el input es insuficiente para operar con seguridad.

## Plantillas de respuesta estructurada

### Plantilla base
```yaml
mode: <diagnose|plan-change|apply-change|verify>
status: <ok|degraded|rejected>
summary: <descripcion breve y precisa>
in_scope_actions:
  - <accion permitida sobre workflows/triggers>
out_of_scope_detected:
  - <elemento rechazado o vacio>
validation:
  pre:
    - <resultado de validacion previa>
  post:
    - <resultado de verificacion posterior o N/A>
rollback:
  plan: <pasos de rollback aplicables>
  readiness: <ready|not-ready>
evidence:
  - <fuente concreta o limitacion declarada>
next_step: <siguiente paso seguro o cierre>
```

### Plantilla de rechazo
```yaml
mode: <modo solicitado>
status: rejected
summary: Solicitud fuera de alcance contractual.
in_scope_actions: []
out_of_scope_detected:
  - <motivo exacto>
validation:
  pre:
    - Rechazo fail-closed aplicado.
  post:
    - N/A
rollback:
  plan: Sin aplicacion de cambios.
  readiness: ready
evidence:
  - Politica del skill: solo workflows y triggers.
next_step: Reformular solicitud dentro de alcance permitido.
```
