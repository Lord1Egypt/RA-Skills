---
name: kansodata-grafana-authoring-operations
description: Opera Grafana en OpenClaw con enfoque seguro: inspección real, diagnóstico, propuesta de cambios y aplicación solo cuando exista tooling habilitado y contexto suficiente.
---

# Skill: kansodata-grafana-authoring-operations

## Propósito

Esta skill guía al agente para:

- inspeccionar estado real de Grafana,
- diagnosticar dashboards y alerting,
- generar/refactorizar JSON de dashboard,
- proponer cambios seguros,
- aplicar cambios solo cuando la herramienta write exista y esté habilitada.

## Modos operativos

1. `inspect_grafana`
- Objetivo: estado base de salud, dashboards, datasources, folders y alert rules.
- Herramientas: `grafana_health_check`, `grafana_list_dashboards`, `grafana_list_datasources`, `grafana_list_alert_rules`, `grafana_list_folders`.

2. `diagnose_dashboard`
- Objetivo: analizar dashboard por UID y detectar señales de rotura o deuda técnica.
- Herramientas: `grafana_get_dashboard`, `grafana_export_dashboard_json`.

3. `generate_dashboard_json`
- Objetivo: producir propuesta JSON para nuevo dashboard (sin aplicar en v1).
- Regla: marcar salida como `draft` o `review_ready` según contexto disponible.

4. `refactor_dashboard_json`
- Objetivo: proponer refactor lógico de dashboard existente.
- Regla: usar estado actual leído desde Grafana antes de proponer.

5. `propose_alert_rule`
- Objetivo: proponer reglas de alerta con justificación y riesgo.
- Regla: no afirmar aplicabilidad sin verificar datasource/queries/contexto.

6. `apply_dashboard_change`
- Objetivo: aplicar cambios en dashboard.
- Estado v1: restringido; requiere herramienta write habilitada y gate activo.

7. `apply_alerting_change`
- Objetivo: aplicar cambios de alerting.
- Estado v1: restringido; requiere herramienta write habilitada y gate activo.

## Niveles de confianza del contexto

- `grafana_state_confirmed`: datos actuales obtenidos por tools read-only.
- `grafana_state_partial`: parte del estado verificado, parte inferido.
- `grafana_state_assumed`: no hay evidencia reciente del entorno.

## Estados de madurez de salida

- `draft`: propuesta preliminar; contexto insuficiente o ambiguo.
- `review_ready`: propuesta consistente para revisión humana.
- `apply_ready`: aplicable técnicamente con tooling/gates habilitados.
- `human_review_required`: cambio sensible o riesgo no mitigado.

## Reglas de comportamiento obligatorias

- Leer estado actual antes de proponer cambios.
- No inventar dashboards, folders, datasources ni alert rules.
- No borrar recursos en v1.
- No afirmar compatibilidad/viabilidad sin verificación real.
- Proponer cambios como diff lógico cuando aplique.
- Pedir operación write solo si existe tool habilitada y contexto suficiente.
- Si falta contexto real, degradar salida a `draft`.

## Degradación segura

- Si falla una tool de lectura: reportar bloqueo y continuar con lo verificable.
- Si el estado es parcial: marcar explícitamente incertidumbre.
- Si se requiere write y no hay gate o tool habilitada: detener y emitir `human_review_required`.

## Casos de uso

1. Listar dashboards disponibles.
2. Revisar dashboard por UID.
3. Exportar JSON para respaldo o versionado lógico.
4. Detectar dashboard roto (queries/panels inválidos observables en JSON).
5. Revisar alert rules existentes.
6. Proponer nueva alerta con justificación.
7. Preparar clon de dashboard como propuesta (sin aplicar en v1).
