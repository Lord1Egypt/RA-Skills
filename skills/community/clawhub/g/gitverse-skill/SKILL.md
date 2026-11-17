---
name: "gitverse-skill"
description: "Own GitVerse (gitverse.ru) skill: repos, issues, PRs via REST API with a dependency-free Python CLI."
---

# gitverse-skill — свой навык для GitVerse

Собственный навык для работы с GitVerse через REST API. Без внешних зависимостей — чистый Python (urllib).

## Setup

```bash
# Токен: https://gitverse.ru/settings/tokens
export GITVERSE_TOKEN="..."        # или положить в ~/.gitverse_token (chmod 600)
```

Скрипт: `scripts/gitverse.py` (или установить в PATH как `gitverse-skill`).

## Usage

```bash
# Репозитории
python3 scripts/gitverse.py repos list                    # свои репозитории
python3 scripts/gitverse.py repos list --org ORG          # репозитории организации
python3 scripts/gitverse.py repos info --owner O --repo R # инфо о репозитории

# Issues
python3 scripts/gitverse.py issues list --owner O --repo R [--state open|closed|all]
python3 scripts/gitverse.py issues view --owner O --repo R --number N
python3 scripts/gitverse.py issues create --owner O --repo R --title "..." [--body "..."]
python3 scripts/gitverse.py issues comment --owner O --repo R --number N --body "..."
python3 scripts/gitverse.py issues close --owner O --repo R --number N

# Pull Requests
python3 scripts/gitverse.py pulls list --owner O --repo R [--state open|closed|all]
python3 scripts/gitverse.py pulls view --owner O --repo R --number N
python3 scripts/gitverse.py pulls create --owner O --repo R --title "..." --head BRANCH --base BRANCH [--body "..."]
python3 scripts/gitverse.py pulls merge --owner O --repo R --number N
```

## Notes

- Base URL по умолчанию: `https://api.gitverse.ru`, переопределяется через `GITVERSE_BASE_URL`
- Заголовок `Accept: application/vnd.gitverse.object+json;version=1`
- Авторизация: `Authorization: Bearer <token>`
- Все команды выводят JSON
- Перед созданием/закрытием/мержем — подтверждать у пользователя, если операция массовая или необратимая
