# Grizzly SMS — MCP Server & OpenClaw Skill

[English](#english) | [Русский](#russian)

---

<a name="english"></a>
## English

MCP (Model Context Protocol) server and **OpenClaw Skill** for integrating with [Grizzly SMS](https://grizzlysms.com/) — a platform for SMS verification codes and virtual phone numbers. Compatible with Cursor, Claude Desktop, OpenClaw (MCP and Skill modes).

### What This Project Provides

| Mode | Description | Use Case |
|------|-------------|----------|
| **MCP Server** | Standards-based MCP server exposing Grizzly API tools | Cursor, Claude Desktop, OpenClaw with mcpServers |
| **OpenClaw Skill** | Instruction-based skill using exec + CLI script | OpenClaw skills-only setup (no mcpServers) |

### Features

#### MCP Server

- **Phone operations:** `request_number`, `get_status`, `set_status`
- **Account:** `get_balance`
- **Info:** `get_countries`, `get_services`, `get_prices`

#### OpenClaw Skill

- **Dialog-based API key:** Bot asks for the key during the conversation
- **Balance & top-up:** Check balance and provide crypto wallet (USDT TRC-20) for top-up
- **Number lifecycle:** Request number, poll for SMS, complete or cancel activation
- **Full registration workflow:** Resolve service/country codes → rent number → open browser → fill forms → enter SMS code
- **Formatted output:** Phone, activation ID, and SMS in copy-friendly format (monospace on Telegram)

### OpenClaw Skill Pipeline

1. **API key** — Bot asks: *Please provide your Grizzly SMS API key*
2. **Balance & top-up** — Bot can show balance and crypto wallet address for USDT TRC-20 top-up
3. **Number** — Bot rents a number for the requested service and country
4. **Status** — Bot can cancel an activation or request a new SMS
5. **SMS** — Bot polls and returns the verification code
6. **Complete** — Bot marks activation complete after code is used

See [CONFIG.md](CONFIG.md) for OpenClaw skill setup.

### Prerequisites

- Node.js 18+
- Grizzly SMS API key — register at [grizzlysms.com](https://grizzlysms.com/), then get it from the [API section](https://grizzlysms.com/docs)

---

### Installation

```bash
git clone https://github.com/GrizzlySMS-Git/grizzly-sms-mcp.git
cd grizzly-sms-mcp
npm install
npm run build
```

---

### Configuration: MCP Server (Cursor, Claude Desktop, OpenClaw mcpServers)

#### Cursor

Location: `%APPDATA%\Cursor\User\globalStorage\mcp.json` (Windows) | `~/Library/Application Support/Cursor/User/globalStorage/mcp.json` (macOS) | `~/.config/Cursor/User/globalStorage/mcp.json` (Linux)

```json
{
  "mcpServers": {
    "grizzly-sms": {
      "command": "node",
      "args": ["/absolute/path/to/grizzly-sms-mcp/dist/index.js"],
      "env": {
        "GRIZZLY_SMS_API_KEY": "your_api_key",
        "GRIZZLY_SMS_BASE_URL": "https://api.grizzlysms.com"
      }
    }
  }
}
```

#### OpenClaw (mcpServers)

Location: `~/.openclaw/openclaw.json` (macOS/Linux) | `%APPDATA%\.openclaw\openclaw.json` (Windows)

```json
{
  "agents": {
    "list": [{
      "id": "main",
      "mcpServers": {
        "grizzly-sms": {
          "command": "node",
          "args": ["/absolute/path/to/grizzly-sms-mcp/dist/index.js"],
          "env": {
            "GRIZZLY_SMS_API_KEY": "your_api_key",
            "GRIZZLY_SMS_BASE_URL": "https://api.grizzlysms.com"
          }
        }
      }
    }
  }
}
```

Use absolute paths. Restart after changes: `openclaw gateway restart`

---

### Configuration: OpenClaw Skill (skills-only, no mcpServers)

1. Add skill path to `openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/absolute/path/to/grizzly-sms-mcp"]
    },
    "entries": {
      "grizzly_sms": {
        "enabled": true
      }
    }
  }
}
```

2. Enable **exec** and optionally **browser** tools for the agent
3. Restart: `npx openclaw gateway restart`

Full setup (exec approvals, browser tool, API key in dialog) — see [CONFIG.md](CONFIG.md).

---

### MCP Tools Reference

| Tool | Parameters | Description |
|------|------------|-------------|
| `request_number` | service (required), country (optional), maxPrice, providerIds, exceptProviderIds | Rent a virtual number |
| `get_status` | activationId (required) | Get activation status and SMS code |
| `set_status` | activationId, status (6=complete, 8=cancel) | Change activation status |
| `get_balance` | — | Check balance |
| `get_wallet` | — | Get USDT TRC-20 wallet address for top-up |
| `get_countries` | — | List countries |
| `get_services` | — | List services |
| `get_prices` | service, country (optional) | Get prices |

### Common Service Codes

| Code | Service |
|------|---------|
| tg | Telegram |
| wa | WhatsApp |
| ig | Instagram |
| fb | Facebook |
| go | Google |
| ub | Uber |

### Common Country IDs

| ID | Country |
|----|---------|
| 73 | Brazil |
| 1 | Ukraine |
| 16 | England |
| 187 | USA |
| 22 | India |

---

### Project Structure

```
grizzly-sms-mcp/
├── SKILL.md           # OpenClaw skill instructions
├── CONFIG.md          # OpenClaw skill config guide
├── clawhub.json       # ClawHub metadata
├── scripts/
│   └── grizzly-cli.mjs # CLI for OpenClaw exec
├── src/               # MCP server (TypeScript)
│   ├── index.ts
│   └── grizzly-sms-client.ts
├── docs/
├── package.json
└── README.md
```

---

### Development

```bash
npm run dev      # Development mode
npm run build    # Build MCP server
npm start        # Run MCP server
npm test         # Run tests
npm run test:api # Test API methods
```

---

### Troubleshooting

- **GRIZZLY_SMS_API_KEY required** — Set in `.env`, config, or provide in chat (Skill mode)
- **BAD_KEY** — Verify API key at [grizzlysms.com](https://grizzlysms.com/)
- **NO_BALANCE** — Top up at [grizzlysms.com](https://grizzlysms.com/) (USDT TRC-20 supported)
- **exec not permitted** — Configure exec approvals; see [CONFIG.md](CONFIG.md)

---

### Support

- API docs: [grizzlysms.com/docs](https://grizzlysms.com/docs)
- Website: [grizzlysms.com](https://grizzlysms.com/)
- Issues: [GitHub Issues](https://github.com/GrizzlySMS-Git/grizzly-sms-mcp/issues)

---

### License

MIT — see [LICENSE](LICENSE)

---

<a name="russian"></a>
## Русский

MCP (Model Context Protocol) сервер и **OpenClaw Skill** для интеграции с [Grizzly SMS](https://grizzlysms.com/) — платформой SMS верификации и виртуальных номеров. Совместимо с Cursor, Claude Desktop, OpenClaw (режимы MCP и Skill).

### Что предоставляет проект

| Режим | Описание | Когда использовать |
|-------|----------|--------------------|
| **MCP Server** | MCP‑сервер с инструментами Grizzly API | Cursor, Claude Desktop, OpenClaw с mcpServers |
| **OpenClaw Skill** | Skill на exec + CLI‑скрипт | OpenClaw только со skills (без mcpServers) |

### Возможности

#### MCP Server

- **Номера:** `request_number`, `get_status`, `set_status`
- **Аккаунт:** `get_balance`
- **Справочники:** `get_countries`, `get_services`, `get_prices`

#### OpenClaw Skill

- **API‑ключ в диалоге:** бот запрашивает ключ в чате
- **Баланс и пополнение:** показывает баланс и криптокошелёк (USDT TRC-20) для пополнения
- **Жизненный цикл номера:** аренда номера, ожидание SMS, завершение или отмена активации
- **Полный workflow регистрации:** определение сервиса/страны → аренда номера → браузер → заполнение форм → ввод SMS‑кода
- **Форматированный вывод:** номер, ID активации и SMS в удобном для копирования виде (моноширинный текст в Telegram)

### Пайплайн OpenClaw Skill

1. **API‑ключ** — бот спрашивает: *Выдайте API ключ Grizzly SMS*
2. **Баланс и пополнение** — бот показывает баланс и адрес кошелька USDT TRC-20
3. **Номер** — бот арендует номер для указанного сервиса и страны
4. **Статус** — бот может отменить активацию или запросить новый SMS
5. **SMS** — бот опрашивает статус и возвращает код
6. **Завершение** — бот помечает активацию выполненной после использования кода

Подробная настройка — в [CONFIG.md](CONFIG.md).

### Требования

- Node.js 18+
- API‑ключ Grizzly SMS — регистрация на [grizzlysms.com](https://grizzlysms.com/), ключ в [разделе API](https://grizzlysms.com/docs)

---

### Установка

```bash
git clone https://github.com/GrizzlySMS-Git/grizzly-sms-mcp.git
cd grizzly-sms-mcp
npm install
npm run build
```

---

### Конфигурация: MCP Server (Cursor, Claude Desktop, OpenClaw mcpServers)

#### Cursor

Путь: `%APPDATA%\Cursor\User\globalStorage\mcp.json` (Windows) | `~/Library/Application Support/Cursor/User/globalStorage/mcp.json` (macOS) | `~/.config/Cursor/User/globalStorage/mcp.json` (Linux)

```json
{
  "mcpServers": {
    "grizzly-sms": {
      "command": "node",
      "args": ["/абсолютный/путь/к/grizzly-sms-mcp/dist/index.js"],
      "env": {
        "GRIZZLY_SMS_API_KEY": "ваш_api_ключ",
        "GRIZZLY_SMS_BASE_URL": "https://api.grizzlysms.com"
      }
    }
  }
}
```

#### OpenClaw (mcpServers)

Путь: `~/.openclaw/openclaw.json` (macOS/Linux) | `%APPDATA%\.openclaw\openclaw.json` (Windows)

```json
{
  "agents": {
    "list": [{
      "id": "main",
      "mcpServers": {
        "grizzly-sms": {
          "command": "node",
          "args": ["/абсолютный/путь/к/grizzly-sms-mcp/dist/index.js"],
          "env": {
            "GRIZZLY_SMS_API_KEY": "ваш_api_ключ",
            "GRIZZLY_SMS_BASE_URL": "https://api.grizzlysms.com"
          }
        }
      }
    }
  }
}
```

Используйте абсолютные пути. После изменений: `openclaw gateway restart`

---

### Конфигурация: OpenClaw Skill (только skills, без mcpServers)

1. Добавьте путь к skill в `openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/абсолютный/путь/к/grizzly-sms-mcp"]
    },
    "entries": {
      "grizzly_sms": {
        "enabled": true
      }
    }
  }
}
```

2. Включите инструменты **exec** и по необходимости **browser**
3. Перезапуск: `npx openclaw gateway restart`

Полная настройка (exec approvals, browser, API key в диалоге) — в [CONFIG.md](CONFIG.md).

---

### Справка по MCP‑инструментам

| Инструмент | Параметры | Описание |
|------------|-----------|----------|
| `request_number` | service (обяз.), country (опц.), maxPrice, providerIds, exceptProviderIds | Аренда виртуального номера |
| `get_status` | activationId (обяз.) | Статус активации и SMS‑код |
| `set_status` | activationId, status (6=завершить, 8=отменить) | Изменение статуса |
| `get_balance` | — | Баланс |
| `get_wallet` | — | Адрес кошелька USDT TRC-20 для пополнения |
| `get_countries` | — | Список стран |
| `get_services` | — | Список сервисов |
| `get_prices` | service, country (опц.) | Цены |

### Коды сервисов

| Код | Сервис |
|-----|--------|
| tg | Telegram |
| wa | WhatsApp |
| ig | Instagram |
| fb | Facebook |
| go | Google |
| ub | Uber |

### ID стран

| ID | Страна |
|----|--------|
| 73 | Бразилия |
| 1 | Украина |
| 16 | Англия |
| 187 | США |
| 22 | Индия |

---

### Решение проблем

- **GRIZZLY_SMS_API_KEY required** — Задайте в `.env`, конфиге или передайте в чате (Skill)
- **BAD_KEY** — Проверьте ключ на [grizzlysms.com](https://grizzlysms.com/)
- **NO_BALANCE** — Пополните на [grizzlysms.com](https://grizzlysms.com/) (USDT TRC-20)
- **exec not permitted** — Настройте exec approvals в [CONFIG.md](CONFIG.md)

---

### Поддержка

- API: [grizzlysms.com/docs](https://grizzlysms.com/docs)
- Сайт: [grizzlysms.com](https://grizzlysms.com/)
- Issues: [GitHub Issues](https://github.com/GrizzlySMS-Git/grizzly-sms-mcp/issues)

---

### Лицензия

MIT — см. [LICENSE](LICENSE)
