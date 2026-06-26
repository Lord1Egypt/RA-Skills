# Ejemplos de ejecución

## search_issue_context
Prompt sugerido:
"Analiza contexto de incidencias críticas del proyecto PROJ en la última semana."

Salida esperada:
- Hechos (issues + estado + prioridad + bloqueos explícitos).
- Inferencias (riesgo de atraso, dependencia probable).
- Datos faltantes.

## summarize_issue
Prompt sugerido:
"Resume PROJ-123 con foco en estado actual y bloqueadores."

Salida esperada:
- Estado factual.
- Comentarios/worklogs relevantes.
- Próximo paso recomendado (sin acción de escritura).

## prepare_status_update
Prompt sugerido:
"Prepara update ejecutivo semanal del backlog de PROJ."

Salida esperada:
- Avances, riesgos, bloqueadores.
- Separación clara entre hechos e inferencias.