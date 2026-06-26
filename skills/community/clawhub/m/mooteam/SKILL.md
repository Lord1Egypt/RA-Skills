---
name: mooteam
description: >
  MooTeam (moo.team) API v1 for OpenClaw: projects, teams, tasks, drafts, comments,
  workflows, statuses, labels, timer and time logs, activity logs. Requires
  MOOTEAM_API_TOKEN and MOOTEAM_COMPANY_ALIAS. Install from ClawHub (clawhub.ai).
user-invokable: true
metadata:
  openclaw:
    emoji: "🐂"
    primaryEnv: MOOTEAM_API_TOKEN
    requires:
      bins: ["python3"]
      env: ["MOOTEAM_API_TOKEN", "MOOTEAM_COMPANY_ALIAS"]
---

# MooTeam

## English (ClawHub)

**MooTeam** is a project / task / CRM API integration. The agent should run the CLI via `exec` using `python3` and paths below.

### Install (community)

1. `clawhub install mooteam` (or your chosen slug after publish) into `<workspace>/skills/`.
2. Install Python deps once (workspace venv recommended):
   `python3 -m pip install -r skills/mooteam/requirements.txt`
3. Set environment variables (gateway `.env`, host env, or `openclaw.json` → `skills.entries.mooteam.env`):
   - `MOOTEAM_API_TOKEN` — Bearer token  
   - `MOOTEAM_COMPANY_ALIAS` — `X-MT-Company` header value  

### How to invoke scripts

- Workspace root as cwd (typical for OpenClaw):  
  `python3 skills/mooteam/scripts/main.py <command> [args]`  
- Or cwd = skill folder (`skills/mooteam`):  
  `python3 scripts/main.py <command> [args]`

Optional: add the workspace `.venv` to `tools.exec.pathPrepend` so `python3` picks up dependencies installed there.

---

## Обзор (RU)

Интерфейс для интеграции с **MooTeam API v1**: проекты, задачи (включая черновики), тайм-трекинг, метки, воркфлоу, логи активности.

## Основные возможности

- **Проекты и команды**: проекты, состав команды на проекте.
- **Задачи и черновики**: задачи, комментарии, черновик → задача.
- **Таймер и время**: один активный таймер; ручные time logs.
- **Справочники**: воркфлоу, статусы, группы меток и метки.
- **Activity logs**: фильтры по проекту, пользователю, типу события.

## Правила для агента

1. **ID из API**: не угадывать ID; при сомнениях — `projects`, `statuses`, `user-profiles`.
2. **Черновик**: перед сложным `task-create` проверить `task-draft`; при готовности — `task-from-draft`.
3. **Таймер**: перед `start` вызвать `timer-current`; при активном таймере на другой задаче — сначала `stop`.
4. **Контекст задачи**: по возможности подтягивать комментарии и time logs.
5. **Списки**: в ответе пользователю — укороченно (`id`, `title`, `status`).

## Структура навыка

- `scripts/MooTeamClient.py` — HTTP-клиент (`requests`).
- `scripts/main.py` — CLI для вызовов из агента.
- `references/api_docs.md` — краткий справочник методов.

## Переменные окружения

- `MOOTEAM_API_TOKEN`
- `MOOTEAM_COMPANY_ALIAS`

## Команды CLI

### Team

Список профилей: `python3 scripts/main.py user-profiles`

### Projects

- Список: `python3 scripts/main.py projects`
- Создать: `python3 scripts/main.py project-create --name "Название" --workflow_id <id>`
- Инфо: `python3 scripts/main.py project-info --id <project_id>`
- Обновить: `python3 scripts/main.py project-update --id <project_id> --name "Имя"`
- Удалить: `python3 scripts/main.py project-delete --id <project_id> --force`
- Добавить в проект: `python3 scripts/main.py project-team-add --project <id> --user <id>`
- Убрать из проекта: `python3 scripts/main.py project-team-remove --map_id <id>`

### Tasks

- Список: `python3 scripts/main.py tasks --project <project_id>`
- Создать: `python3 scripts/main.py task-create --project <id> --header "Заголовок" --user_id <executor_id>`
- Инфо: `python3 scripts/main.py task-info --id <task_id>`
- Обновить: `python3 scripts/main.py task-update --id <id> --header "..."` (опционально `--status_id`)
- Удалить: `python3 scripts/main.py task-delete --id <task_id>`

### Drafts

- Текущий черновик: `python3 scripts/main.py task-draft`
- Обновить: `python3 scripts/main.py task-draft-update --header "..." --project <id>`
- Задача из черновика: `python3 scripts/main.py task-from-draft`

### Comments

- Список: `python3 scripts/main.py comments --task_id <id>`
- Создать: `python3 scripts/main.py comment-create --task_id <id> --text "..."`
- Удалить: `python3 scripts/main.py comment-delete --id <comment_id>`

### Workflows & statuses

- Воркфлоу: `python3 scripts/main.py workflows` / `workflow-create` / `workflow-info` / `workflow-update` / `workflow-delete`
- Статусы: `python3 scripts/main.py statuses` и `status-create|status-info|status-update|status-delete`

### Labels

- Группы: `label-groups`, `label-group-create|update|delete`
- Метки: `labels`, `label-create|label-info|label-update|label-delete`

### Timer & time logs

- `timer-current`, `start <task_id>`, `stop`
- `time-create|time-update|time-delete`, `task-time --task_id <id>`, `time-list`

### Activity

- `activity` (опции `--project`, `--user`, `--type`)
- `activity-projects`

## Примеры запросов пользователя

- «Покажи проекты и добавь задачу … в проект X»
- «Сколько времени по задаче #…»
- «Лог активности по проекту …»
- «Запусти таймер на задаче …»
