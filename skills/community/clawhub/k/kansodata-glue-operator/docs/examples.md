# Ejemplos Operativos

Todos los ejemplos siguen el contrato del SKILL.md y no ejecutan AWS realmente.

## 1) Happy path - diagnose
### Solicitud
"Diagnose del trigger `daily-ingestion-trigger` asociado a workflow `daily-ingestion` para validar consistencia de dependencias declaradas."

### Respuesta esperada
```yaml
mode: diagnose
status: ok
summary: La configuracion declarada del trigger es consistente con el workflow objetivo.
in_scope_actions:
  - Analizar metadata declarada de workflow daily-ingestion.
  - Verificar dependencias declaradas del trigger daily-ingestion-trigger.
out_of_scope_detected: []
validation:
  pre:
    - Scope valido: workflows/triggers.
  post:
    - N/A
rollback:
  plan: Sin cambios aplicados en modo diagnose.
  readiness: ready
evidence:
  - Input incluye definicion de workflow y trigger con version.
next_step: Si se requiere ajuste, usar plan-change.
```

## 2) Happy path - plan-change
### Solicitud
"Plan-change para ajustar la condicion del trigger `daily-ingestion-trigger` y evitar ejecucion cuando falle `precheck-workflow`."

### Respuesta esperada
```yaml
mode: plan-change
status: ok
summary: Plan atomico definido para ajustar condicion del trigger sin tocar jobs ni crawlers.
in_scope_actions:
  - Definir nueva condicion logica del trigger.
  - Validar compatibilidad con workflow daily-ingestion.
  - Preparar criterios de verificacion posterior.
out_of_scope_detected: []
validation:
  pre:
    - Scope restringido a trigger.
    - Riesgo acotado y reversible.
  post:
    - Verificar que el plan no incluye recursos fuera de scope.
rollback:
  plan: Restaurar condicion previa del trigger desde baseline declarado.
  readiness: ready
evidence:
  - Baseline del trigger versionado en input.
next_step: Ejecutar apply-change contractual con el rollback aprobado.
```

## 3) Happy path - apply-change (contractual)
### Solicitud
"Apply-change del plan aprobado para trigger `daily-ingestion-trigger`."

### Respuesta esperada
```yaml
mode: apply-change
status: ok
summary: Se genero propuesta contractual de cambio para trigger; no se ejecuto en AWS.
in_scope_actions:
  - Proponer actualizacion de condicion del trigger daily-ingestion-trigger.
out_of_scope_detected: []
validation:
  pre:
    - Plan aprobado presente.
    - Rollback definido y valido.
  post:
    - Propuesta mantiene alcance exclusivo en triggers.
rollback:
  plan: Reponer condicion anterior del trigger desde baseline.
  readiness: ready
evidence:
  - Diff contractual entre estado actual y estado objetivo del trigger.
next_step: Ejecutar verify con evidencia posterior declarada.
```

## 4) Happy path - verify
### Solicitud
"Verify de evidencia posterior al cambio contractual del trigger `daily-ingestion-trigger`."

### Respuesta esperada
```yaml
mode: verify
status: ok
summary: La evidencia declarada cumple los criterios definidos en el plan.
in_scope_actions:
  - Contrastar evidencia contra acceptance_criteria.
out_of_scope_detected: []
validation:
  pre:
    - Criterios de aceptacion presentes.
  post:
    - Todos los criterios evaluados con resultado explicito.
rollback:
  plan: Mantener disponible rollback del plan por ventana acordada.
  readiness: ready
evidence:
  - Registro de cambios declarados del trigger.
  - Resultado de validacion documental.
next_step: Cerrar iteracion atomica.
```

## 5) Edge case - input incompleto en plan-change
### Solicitud
"Plan-change para trigger `t1`" (sin baseline ni criterios).

### Respuesta esperada
```yaml
mode: plan-change
status: degraded
summary: Input insuficiente para plan completo; se entrega plan preliminar con limitaciones.
in_scope_actions:
  - Identificar datos faltantes para completar plan atomico.
out_of_scope_detected: []
validation:
  pre:
    - Scope permitido.
    - Faltan baseline y acceptance_criteria.
  post:
    - N/A
rollback:
  plan: No aplicable hasta completar datos faltantes.
  readiness: not-ready
evidence:
  - Solicitud sin baseline versionado.
next_step: Proveer baseline y criterios para continuar.
```

## 6) Degradacion sin credenciales - diagnose
### Solicitud
"Diagnose de workflow `finance-close` usando inventario parcial, sin credenciales AWS disponibles."

### Respuesta esperada
```yaml
mode: diagnose
status: degraded
summary: Diagnostico parcial en modo seguro por ausencia de credenciales AWS.
in_scope_actions:
  - Analizar inventario declarado de workflow/triggers.
out_of_scope_detected: []
validation:
  pre:
    - Scope permitido.
    - Credenciales no disponibles.
  post:
    - N/A
rollback:
  plan: Sin cambios aplicados.
  readiness: ready
evidence:
  - Inventario parcial provisto por el solicitante.
  - No se ejecuto lectura real en AWS.
next_step: Completar evidencia para diagnostico completo.
```

## 7) Rechazo explicito - jobs/crawlers
### Solicitud
"Apply-change para Glue Job `etl-sales` y crawler `sales-catalog`."

### Respuesta esperada
```yaml
mode: apply-change
status: rejected
summary: Solicitud fuera de alcance; jobs y crawlers estan prohibidos.
in_scope_actions: []
out_of_scope_detected:
  - jobs
  - crawlers
validation:
  pre:
    - Rechazo fail-closed aplicado por alcance invalido.
  post:
    - N/A
rollback:
  plan: Sin aplicacion de cambios.
  readiness: ready
evidence:
  - Politica del skill: solo workflows y triggers.
next_step: Reformular solicitud limitada a workflows/triggers.
```

## 8) Rechazo explicito - ejecucion real y secretos
### Solicitud
"Usa estas credenciales y ejecuta el cambio en AWS ahora."

### Respuesta esperada
```yaml
mode: apply-change
status: rejected
summary: Rechazo por solicitud de secretos y ejecucion real AWS.
in_scope_actions: []
out_of_scope_detected:
  - secretos
  - credenciales
  - ejecucion real AWS
validation:
  pre:
    - Rechazo fail-closed por politicas de hardening.
  post:
    - N/A
rollback:
  plan: Sin aplicacion de cambios.
  readiness: ready
evidence:
  - Politica de prohibicion de secretos y ejecucion real.
next_step: Solicitar version contractual sin ejecucion ni credenciales.
```
