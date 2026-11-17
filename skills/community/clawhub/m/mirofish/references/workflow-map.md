# MiroFish Workflow Map

## Distilled workflow

Seed material -> ontology -> simulation plan -> forecast report -> interviews

Use this offline path by default. The repository-backed stages below are only for live backend execution.

## Repository-backed stages

### 1. Graph stage

- `POST /api/graph/ontology/generate`
- `POST /api/graph/build`
- `GET /api/graph/project/<project_id>`
- `GET /api/graph/task/<task_id>`
- `GET /api/graph/data/<graph_id>`

### 2. Simulation stage

- `POST /api/simulation/create`
- `POST /api/simulation/prepare`
- `POST /api/simulation/start`
- `POST /api/simulation/generate-profiles`
- `POST /api/simulation/<simulation_id>/run-status`
- `POST /api/simulation/<simulation_id>/timeline`
- `POST /api/simulation/<simulation_id>/comments`
- `POST /api/simulation/<simulation_id>/posts`
- `POST /api/simulation/<simulation_id>/agent-stats`

### 3. Report stage

- `POST /api/report/generate`
- `POST /api/report/generate/status`
- `GET /api/report/<report_id>`
- `GET /api/report/by-simulation/<simulation_id>`
- `GET /api/report/<report_id>/progress`
- `GET /api/report/<report_id>/sections`
- `POST /api/report/chat`

### 4. Interview stage

- `POST /api/simulation/interview`
- `POST /api/simulation/interview/batch`
- `POST /api/simulation/interview/all`
- `POST /api/simulation/interview/history`
- `POST /api/simulation/env-status`
- `POST /api/simulation/close-env`

## Practical interpretation

- Use the graph stage to extract and formalize the scenario.
- Use the simulation stage to generate a believable parallel world with agents and memory.
- Use the report stage to produce the forecast narrative and evidence trail.
- Use the interview stage to probe the simulated world after the report exists.
