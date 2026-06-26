# 🔍 li_sentry_check - Навык инспекции серверов

> Кроссплатформенный навык инспекции и проверки здоровья серверов. Подключение SSH к удалённым Linux-серверам с аутентификацией по ключу, выполнение команд инспекции только для чтения и генерация структурированных отчётов в Markdown.

[![Версия](https://img.shields.io/badge/версия-0.1.0-blue.svg)](https://clawhub.ai/skills/li_sentry_check)
[![Платформы](https://img.shields.io/badge/платформы-nanobot%20%7C%20OpenClaw%20%7C%20Hermes-green.svg)]()
[![Лицензия](https://img.shields.io/badge/лицензия-MIT-green.svg)](LICENSE)

## 📋 Обзор

`li_sentry_check` — это кроссплатформенный навык инспекции серверов, поддерживающий **nanobot**, **OpenClaw** и **Hermes agent**. Он подключается к удалённым Linux-серверам через SSH-аутентификацию по ключу, выполняет команды инспекции только для чтения (CPU, память, диск, сеть, сервисы, безопасность) и генерирует структурированные Markdown-отчёты с автоматическим выделением аномалий.

## ✨ Основные функции

| Функция | Описание |
|---------|----------|
| 🔐 SSH-аутентификация по ключу | Только аутентификация по ключу, вход по паролю отключён, безопасность усилена |
| 📊 Инспекция оборудования | CPU, память, диск, использование сети |
| 🖥️ Инспекция сервисов | Состояние ключевых сервисов, журналы ошибок |
| 🛡️ Инспекция безопасности | Аномальные SSH-входы, предупреждения фаервола, ошибки ядра |
| 📝 Структурированные отчёты | Формат Markdown/JSON, аномалии в приоритете |
| 🌐 Кроссплатформенность | Поддерживает nanobot, OpenClaw, Hermes |

## 🚀 Быстрый старт

### 1. Установка навыка

```bash
# nanobot
./manage.sh skill install li_sentry_check

# OpenClaw
npx clawhub@latest install li_sentry_check

# Hermes
hermes skill install li_sentry_check
```

### 2. Настройка SSH-ключей

```bash
# Генерация пары ключей
ssh-keygen -t rsa -b 4096 -f ~/.ssh/li_sentry_check -N ""

# Копирование открытого ключа на удалённый сервер
ssh-copy-id -i ~/.ssh/li_sentry_check.pub inspector@<IP_СЕРВЕРА>

# Тест подключения
ssh -i ~/.ssh/li_sentry_check inspector@<IP_СЕРВЕРА>
```

### 3. Настройка целевых серверов

Редактировать `references/targets.yaml`:

```yaml
targets:
  production-web:
    host: ВАШ_IP_СЕРВЕРА
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - nginx
      - docker
      - sshd
```

### 4. Запуск инспекции

```bash
# Базовая инспекция (аппаратные ресурсы)
python3 scripts/inspect.py --target production-web --checks basic

# Инспекция сервисов
python3 scripts/inspect.py --target production-web --checks services

# Полная инспекция (базовая + сервисы + безопасность + журналы)
python3 scripts/inspect.py --target production-web --checks daily

# Вывод в формате JSON
python3 scripts/inspect.py --target production-web --checks daily --format json

# Вывод в файл
python3 scripts/inspect.py --target production-web --checks daily --output report.md
```

## 📖 Группы проверок инспекции

| Группа | Содержимое | Команды |
|--------|------------|---------|
| `basic` | CPU, память, диск, сеть | 8 |
| `services` | Состояние сервисов + журналы ошибок (динамически) | 3×N |
| `daily` | Полная инспекция (базовая + сервисы + безопасность + журналы) | 26 |

## 📊 Пример отчёта

```markdown
# 🔍 Отчёт об инспекции сервера

- Цель: production-web
- Хост: ВАШ_IP_СЕРВЕРА
- Пользователь: inspector
- Проверки: daily
- Запущен: 2026-04-26T09:00:00+00:00
- Всего проверок: 26
- ⚠️ Аномалий: 3

## Общий статус: ⚠️ ПРЕДУПРЕЖДЕНИЕ

## ⚠️ Аномалии (Приоритет)

### ⚠️ systemd_failed_units
Команда: `systemctl --failed --no-pager`
Статус: OK (содержит аномалии)

Вывод:
```
UNIT          LOAD   ACTIVE SUB    DESCRIPTION
mcelog.service loaded failed failed Machine Check Exception Logging Daemon
```
```

## 🔧 Параметры командной строки

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `--target` | Имя целевого сервера (определён в targets.yaml) | (обязательно) |
| `--checks` | Группа проверок: `basic`, `services`, `daily` | `basic` |
| `--format` | Формат вывода: `markdown`, `json` | `markdown` |
| `--output` | Вывод в файл (по умолчанию: stdout) | stdout |

## 🌐 Кроссплатформенная поддержка

| Платформа | Среда выполнения | Скрипт | Команда |
|-----------|------------------|--------|---------|
| **OpenClaw** | Node.js 24+ | `scripts/inspect.mjs` | `node scripts/inspect.mjs --target bogon --checks daily` |
| **NanoBot** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |
| **Hermes** | Python 3.10+ | `scripts/inspect.py` | `python3 scripts/inspect.py --target bogon --checks daily` |

## 📁 Структура файлов

```
li_sentry_check/
├── SKILL.md                  # Документация навыка
├── _meta.json                # Метаданные навыка
├── design.md                 # Документация дизайна
├── references/
│   ├── targets.yaml          # Настройка целевых серверов
│   └── checks.yaml           # Белый список команд инспекции
└── scripts/
    ├── inspect.mjs           # Реализация на Node.js (OpenClaw)
    └── inspect.py            # Реализация на Python (NanoBot/Hermes)
```

## 🔒 Лучшие практики безопасности

- **Права на ключ**: `chmod 600 ~/.ssh/li_sentry_check`
- **Проверка хоста**: Для продакшена предварительно заполните `known_hosts` вместо использования `accept-new`
- **Имена сервисов**: Только буквенно-цифровые символы, дефисы, подчёркивания (проверяются перед использованием)
- **Белый список команд**: Никогда не модифицируйте `checks.yaml` командами, изменяющими состояние
- **Обработка отчётов**: Отчёты могут содержать системные данные — не публикуйте их публично

## 🔧 Руководство по расширению

### Добавление нового целевого сервера

Редактировать `references/targets.yaml`:

```yaml
targets:
  сервер-базы-данных:
    host: ВАШ_IP_СЕРВЕРА
    port: 22
    user: inspector
    keyPath: ~/.ssh/li_sentry_check
    services:
      - mysql
      - redis
```

### Добавление новой группы проверок

Редактировать `references/checks.yaml`:

```yaml
checks:
  база-данных:
    description: Инспекция базы данных
    commands:
      - id: mysql_status
        cmd: "systemctl status mysql --no-pager | sed -n '1,20p'"
        timeoutSec: 10
      - id: mysql_connections
        cmd: "mysql -e 'SHOW STATUS LIKE \"Threads_connected\"' || true"
        timeoutSec: 15
```

## 📝 История версий

| Версия | Дата | Изменения |
|--------|------|-----------|
| 0.1.0 | 2026-04-26 | Первоначальный релиз: базовая, сервисная и полная инспекция |

## 📄 Лицензия

Лицензия MIT
