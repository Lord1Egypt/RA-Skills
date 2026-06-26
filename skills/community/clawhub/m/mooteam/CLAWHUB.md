# Публикация на ClawHub (clawhub.ai)

Эта папка — **готовый бандл** для загрузки в реестр: только `SKILL.md`, `scripts/*.py`, `requirements.txt` и `references/`, без vendored-зависимостей в `scripts/`.

## Проверка локально

Из корня воркспейса (после копирования `clawhub` как `skills/mooteam` или с symlink):

```bash
python3 -m pip install -r skills/mooteam/requirements.txt
export MOOTEAM_API_TOKEN=...
export MOOTEAM_COMPANY_ALIAS=...
python3 skills/mooteam/scripts/main.py projects
```

## Команда publish

Из каталога **`skills/mooteam`** (родитель этой папки):

```bash
npx clawhub@latest publish ./clawhub \
  --slug mooteam \
  --name "MooTeam" \
  --version 1.0.0 \
  --tags latest,crm,tasks,project-management,api \
  --changelog "Initial community release: API v1 CLI (projects, tasks, timer, activity)."
```

При обновлении версии увеличьте semver и опишите изменения в `--changelog`.

## После публикации

В описании на сайте можно кратко указать: нужны `MOOTEAM_API_TOKEN` и `MOOTEAM_COMPANY_ALIAS`, установка зависимостей: `pip install -r requirements.txt` в каталоге навыка.

## OpenClaw `openclaw.json` (пример)

Пользователи могут включить навык и пробросить переменные:

```json
"skills": {
  "entries": {
    "mooteam": {
      "enabled": true,
      "apiKey": "${MOOTEAM_API_TOKEN}",
      "env": {
        "MOOTEAM_COMPANY_ALIAS": "${MOOTEAM_COMPANY_ALIAS}"
      }
    }
  }
}
```

Точная схема полей зависит от версии OpenClaw; главное — чтобы обе переменные были доступны процессу gateway / агента.
