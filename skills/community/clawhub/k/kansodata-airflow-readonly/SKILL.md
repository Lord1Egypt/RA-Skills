# Airflow Read-Only Skill

## Propósito
Esta skill permite consultar Apache Airflow mediante la Stable REST API `/api/v2` en modo solo lectura.
Está diseñada para inspección operativa y diagnóstico, sin ejecutar mutaciones sobre DAGs, runs ni tasks.

## Cuándo usar esta skill
Usa esta skill cuando necesites:
- Listar DAGs disponibles.
- Revisar ejecuciones (DAG runs) de un DAG específico.
- Revisar task instances dentro de un DAG run específico.

No uses esta skill para:
- Disparar ejecuciones de DAG.
- Pausar, reanudar, borrar o modificar recursos.
- Cambiar configuración de Airflow.

## Prerrequisitos
Antes de usarla, confirma:
- El plugin `@kansodata/openclaw-airflow-plugin` está instalado y activo en OpenClaw.
- Existe configuración válida para conexión al host de Airflow.
- Existe autenticación válida (por ejemplo, bearer token) para consultar `/api/v2`.

Si falta configuración o credenciales, repórtalo explícitamente y no improvises valores.

## Tools disponibles (mapeo exacto)
Esta skill usa únicamente estas tools del plugin:
- `airflow.list_dags`
- `airflow.list_dag_runs`
- `airflow.list_task_instances`

No asumas ni menciones tools adicionales.

## Flujo recomendado
Sigue este orden para mantener contexto y trazabilidad:
1. Descubrir DAG con `airflow.list_dags`.
2. Consultar ejecuciones del DAG con `airflow.list_dag_runs` usando `dag_id` exacto.
3. Consultar tasks del run con `airflow.list_task_instances` usando `dag_id` y `dag_run_id` exactos.

Si un paso no devuelve datos, informa el resultado y detén el encadenamiento hasta confirmar el identificador correcto.

## Reglas operativas
- Mantén el comportamiento estrictamente read-only.
- No prometas acciones de escritura ni cambios de estado.
- No asumas estados cuando faltan datos.
- Usa identificadores exactos (`dag_id`, `dag_run_id`) sin normalizaciones inventadas.
- Entrega respuestas compactas y accionables.
- Si no hay resultados, decláralo claramente.
- Si hay error de autenticación o configuración, repórtalo tal cual.

## Límites y seguridad
- Alcance limitado a consultas de lectura sobre Airflow `/api/v2`.
- Prohibido sugerir o simular mutaciones (trigger, pause, delete, patch, update).
- Ante errores de auth/config/host, prioriza transparencia del error sobre respuestas especulativas.

## Estilo de salida esperado
- Resumen corto al inicio.
- Listas breves cuando aplique.
- Identificadores exactos cuando existan.
- Sin ruido ni texto decorativo.

## Ejemplos de prompts (español)
- "Lista los DAGs disponibles en Airflow y muéstrame solo `dag_id` y estado."
- "Para el DAG `daily_ingestion`, dame los últimos 5 DAG runs ordenados por fecha."
- "En el DAG run `scheduled__2026-04-08T03:00:00+00:00` de `daily_ingestion`, lista task instances con estado y duración."
- "Primero busca DAGs que contengan `sales`, luego toma el DAG más relevante, revisa sus runs más recientes y finalmente muestra las tasks del último run fallido."
- "Consulta `airflow.list_dag_runs` para `finance_etl` y si no hay resultados, indícalo explícitamente sin asumir errores."
