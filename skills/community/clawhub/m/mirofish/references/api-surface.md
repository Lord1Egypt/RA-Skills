# API Surface

## Graph

- `POST /api/graph/ontology/generate`
- `POST /api/graph/build`
- `GET /api/graph/project/<project_id>`
- `GET /api/graph/project/list`
- `POST /api/graph/project/<project_id>/reset`
- `GET /api/graph/task/<task_id>`
- `GET /api/graph/tasks`
- `GET /api/graph/data/<graph_id>`
- `DELETE /api/graph/delete/<graph_id>`

## Simulation

- `POST /api/simulation/create`
- `POST /api/simulation/prepare`
- `POST /api/simulation/generate-profiles`
- `POST /api/simulation/start`
- `POST /api/simulation/stop`
- `POST /api/simulation/env-status`
- `POST /api/simulation/close-env`
- `POST /api/simulation/interview`
- `POST /api/simulation/interview/batch`
- `POST /api/simulation/interview/all`
- `POST /api/simulation/interview/history`
- `POST /api/simulation/<simulation_id>/config`
- `POST /api/simulation/<simulation_id>/config/realtime`
- `POST /api/simulation/<simulation_id>/config/download`
- `POST /api/simulation/<simulation_id>/profiles`
- `POST /api/simulation/<simulation_id>/profiles/realtime`
- `POST /api/simulation/<simulation_id>/run-status`
- `POST /api/simulation/<simulation_id>/run-status/detail`
- `POST /api/simulation/<simulation_id>/timeline`
- `POST /api/simulation/<simulation_id>/history`
- `POST /api/simulation/<simulation_id>/comments`
- `POST /api/simulation/<simulation_id>/posts`
- `POST /api/simulation/<simulation_id>/actions`
- `POST /api/simulation/<simulation_id>/agent-stats`
- `POST /api/simulation/script/<script_name>/download`
- `POST /api/simulation/entities/<graph_id>`
- `POST /api/simulation/entities/<graph_id>/<entity_uuid>`
- `POST /api/simulation/entities/<graph_id>/by-type/<entity_type>`

## Report

- `POST /api/report/generate`
- `POST /api/report/generate/status`
- `GET /api/report/<report_id>`
- `GET /api/report/by-simulation/<simulation_id>`
- `GET /api/report/list`
- `GET /api/report/<report_id>/download`
- `DELETE /api/report/<report_id>`
- `POST /api/report/chat`
- `GET /api/report/<report_id>/progress`
- `GET /api/report/<report_id>/sections`
- `GET /api/report/<report_id>/section/<int:section_index>`
- `GET /api/report/<report_id>/agent-log`
- `GET /api/report/<report_id>/agent-log/stream`
- `GET /api/report/<report_id>/console-log`
- `GET /api/report/<report_id>/console-log/stream`
- `POST /api/report/tools/search`
- `POST /api/report/tools/statistics`
- `GET /api/report/check/<simulation_id>`
