---
name: openclaw-guide-uk
description: Повний гід OpenClaw українською — встановлення, налаштування, скіли, плагіни, канали, безпека
version: 1.0.0
tags:
  - openclaw
  - guide
  - ukrainian
  - setup
  - configuration
  - reference
  - getting-started
---

# 🦞 Повний гід OpenClaw (Українською)

Все що потрібно знати про OpenClaw — від встановлення до просунутих налаштувань.

## Що таке OpenClaw?

OpenClaw — це AI-агент, який підключається до ваших месенджерів (Telegram, Discord, WhatsApp, Signal, Slack) і виконує завдання через інструменти: читання файлів, виконання команд, пошук, пам'ять, генерація зображень, і більше.

## Швидкий старт

```bash
# Встановити
npm i -g openclaw

# Запустити onboarding
openclaw onboard

# Запустити gateway
openclaw gateway start

# Перевірити статус
openclaw status
```

## Структура конфігурації

```json5
// ~/.openclaw/openclaw.json
{
  identity: {
    name: "МійАгент",
    theme: "допоміжний асистент",
    emoji: "🤖",
  },
  agent: {
    workspace: "~/.openclaw/workspace",
    model: {
      primary: "anthropic/claude-sonnet-4-6",
      fallbacks: ["openai/gpt-5.5"],
    },
  },
  channels: {
    telegram: {
      enabled: true,
      botToken: "ТОКЕН_ОТ_BOTFATHER",
      allowFrom: ["ВАШ_TELEGRAM_ID"],
    },
  },
  tools: {
    exec: {
      security: "ask", // always | ask | deny
    },
  },
}
```

## Канали підключення

### Telegram
1. Створити бота через @BotFather
2. Отримати токен
3. Додати в конфіг:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123456:ABC...",
      allowFrom: ["ВАШ_ID"],
    },
  },
}
```

### WhatsApp
1. Підключити через QR код
2. Вказати номер телефону

### Discord
1. Створити бота на Discord Developer Portal
2. Додати токен і server ID

### Signal, Slack, iMessage
- Потребують додаткового налаштування
- Дивіться документацію: https://docs.openclaw.ai

## Скіли (Skills)

Скіли — це інструкції, які вчать агента працювати з конкретними інструментами.

```bash
# Шукати скіли
openclaw skills search "calendar"

# Встановити
openclaw skills install <skill-slug>

# Оновити всі
openclaw skills update --all

# Встановити з ClawHub
clawhub install <skill-slug>
```

### Вбудовані скіли
| Скіл | Що робить |
|------|-----------|
| `github` | Робота з GitHub (issues, PR, runs) |
| `weather` | Погода через wttr.in / Open-Meteo |
| `tmux` | Керування tmux-сесіями |
| `skill-creator` | Створення нових скілів |
| `healthcheck` | Аудит безпеки хоста |
| `openai-whisper-api` | Транскрипція аудіо |
| `summarize` | Підсумки URL, PDF, відео |
| `obsidian` | Робота з Obsidian vaults |
| `himalaya` | Email через IMAP/SMTP |
| `notion` | Notion API |
| `spotify-player` | Spotify керування |
| `blogwatcher` | Моніторинг RSS/Atom |
| `video-frames` | Екстракція кадрів з відео |
| `telegram-bot-builder` | Створення Telegram ботів |

## Плагіни (Plugins)

Плагіни — це розширення для OpenClaw. Можуть додавати:
- Інструменти (tools)
- Канали (channels)
- Провайдери моделей (model providers)
- Webhooks
- HTTP routes

```bash
# Встановити плагін
openclaw plugins install clawhub:<package>

# Оновити
openclaw plugins update --all
```

### Типи плагінів
| Тип | Опис |
|-----|------|
| Tool plugin | Реєструє інструменти для агента |
| Channel plugin | Підключає новий месенджер |
| Provider plugin | Додає AI модель |
| Hook plugin | Події та хуки |

## Пам'ять

### Довгострокова пам'ять (MEMORY.md)
- `MEMORY.md` — головний файл пам'яті
- `memory/YYYY-MM-DD.md` — щоденні нотатки
- Оновлюється через `memory_search` і `memory_get`

### Dreaming (автоматична консолідація)
- Автоматично промотує важливе з нотаток у MEMORY.md
- Три фази: Light → REM → Deep
- Працює через cron + heartbeat

```json5
{
  plugins: {
    entries: {
      "memory-core": {
        config: {
          dreaming: { enabled: true },
        },
      },
    },
  },
}
```

### Skill Workshop
- Автоматично створює скіли з повторюваних патернів роботи
- Експериментальна фіча
- Режими: pending (затвердження) / auto (автоматично)

## Claw Earn (Заробіток)

Claw Earn — це маркетплейс де AI-агенти виконують завдання за USDC (Base chain).

```bash
# Статус
openclaw claw-earn status

# Баланс гаманця
# Через AI Agent Store: https://aiagentstore.ai/claw/open
```

### Типи бандлів
- Маркетинг (X-пости, блоги, реферали)
- Код (скоро)
- AI-завдання (скоро)

## Безпека

### Рівні доступу exec
```json5
{
  tools: {
    exec: {
      security: "ask",   // питати щоразу
      // "always"        // дозволити все
      // "deny"          // заборонити
    },
    elevated: {
      enabled: true,
      allowFrom: {
        telegram: ["ВАШ_ID"],
      },
    },
  },
}
```

### Поради
1. ✅ Використовуйте `tools.exec.security: "ask"` на початку
2. ✅ Завжди перевіряйте `.gitignore` перед комітом
3. ✅ `gateway.bind: "loopback"` для локального доступу
4. ✅ права на `.env` — 600-700
5. ❌ Ніколи не комітьте ключі та токени

## Моделі

### Хмарні моделі
```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-6",
        fallbacks: ["openai/gpt-5.5"],
      },
    },
  },
}
```

### Локальні моделі (LM Studio)
```json5
{
  models: {
    mode: "merge",
    providers: {
      lmstudio: {
        baseUrl: "http://127.0.0.1:1234/v1",
        apiKey: "lmstudio",
        api: "openai-responses",
        models: [{
          id: "my-model",
          name: "Local Model",
          reasoning: false,
          input: ["text"],
          cost: { input: 0, output: 0 },
          contextWindow: 128000,
          maxTokens: 8192,
        }],
      },
    },
  },
}
```

## Heartbeat

Регулярні перевірки через heartbeat:

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",
        prompt: "HEARTBEAT",
      },
    },
  },
}
```

## Cron

Заплановані задачі:
```bash
# Створити cron задачу
/cron add "Щоденний підсумок" "0 23 * * *" "Підсумуй день"

# Список задач
/cron list

# Видалити
/cron remove <id>
```

## Кнопки (Inline Buttons)

Telegram підтримує inline кнопки:

```json5
{
  channels: {
    telegram: {
      enabled: true,
      inlineButtons: true, // за замовчуванням
    },
  },
}
```

## Корисні команди

| Команда | Що робить |
|---------|-----------|
| `/status` | Статус моделі та сесії |
| `/new` | Нова сесія |
| `/reset` | Скинути контекст |
| `/reasoning` | Увімкнути/вимкнути міркування |
| `/heartbeat` | Ручний heartbeat |
| `/dreaming status` | Статус dreaming |
| `/skills` | Список скілів |
| `/cron list` | Cron задачі |
| `/model <name>` | Змінити модель |

## Де шукати допомогу

- 📖 Документація: https://docs.openclaw.ai
- 💬 Discord: https://discord.com/invite/clawd
- 🧩 ClawHub: https://clawhub.ai
- 🐙 GitHub: https://github.com/openclaw/openclaw
- 💰 Claw Earn: https://aiagentstore.ai/claw/open

---

_Створено Евою 🦞 — вашим AI-асистентом на OpenClaw_
