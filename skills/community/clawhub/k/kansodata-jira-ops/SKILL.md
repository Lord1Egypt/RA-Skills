---
name: kansodata-jira-ops
description: Skill operativa read-only para análisis de Jira Cloud con enfoque en contexto, bloqueadores y triage.
---

# Skill: kansodata-jira-ops

## Propósito
Analizar contexto operativo en Jira Cloud con evidencia verificable, sin ejecutar acciones de escritura.

## Alcance
Esta skill solo usa tools read-only del plugin Jira:
- `get_issue`
- `search_issues`
- `get_issue_comments`
- `get_issue_worklogs`
- `get_project`
- `list_projects`
- `list_issue_types`
- `list_statuses`
- `list_transitions`

## Prohibiciones
- No inventar datos.
- No ejecutar writes (crear, editar, comentar, asignar, transicionar).
- No presentar inferencias como hechos.

## Regla de salida obligatoria
Separar siempre:
1. Hechos observados (evidencia de Jira).
2. Inferencias (hipótesis razonables).
3. Datos faltantes / permisos insuficientes.

## Modos operativos

### 1) search_issue_context
Objetivo: reunir contexto de una o varias issues.
Pasos mínimos:
1. Buscar issues con `search_issues`.
2. Profundizar con `get_issue` para las claves críticas.
3. Agregar comentarios/worklogs si aportan señal.

### 2) summarize_issue
Objetivo: resumir estado actual de una issue.
Pasos mínimos:
1. `get_issue`.
2. `get_issue_comments`.
3. `get_issue_worklogs`.
Salida mínima:
- Resumen factual, riesgos, próximos pasos sugeridos (sin escribir en Jira).

### 3) analyze_blockers
Objetivo: detectar bloqueadores explícitos e implícitos.
Pasos mínimos:
1. `search_issues` con JQL orientado a bloqueos.
2. `get_issue` en candidatas.
3. Clasificar bloqueadores por criticidad y dependencia.

### 4) triage_backlog
Objetivo: priorizar backlog por impacto/urgencia.
Pasos mínimos:
1. `search_issues` del backlog objetivo.
2. Revisar campos clave (priority, status, assignee, labels).
3. Entregar propuesta de triage indicando qué es hecho vs inferencia.

### 5) prepare_status_update
Objetivo: preparar update de estado para stakeholders sin modificar Jira.
Pasos mínimos:
1. Consolidar issues por objetivo/sprint/proyecto.
2. Identificar avances, riesgos, bloqueadores.
3. Producir texto listo para enviar fuera de Jira.

## Degradación segura
Si faltan permisos o datos:
- No forzar conclusiones.
- Informar exactamente qué endpoint falló y por qué.
- Entregar alternativa conservadora con datos parciales.

## Ejemplos
Ver `examples.md` en esta misma carpeta.