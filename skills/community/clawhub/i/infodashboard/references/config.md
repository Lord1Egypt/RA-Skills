# Configure Environment

## Critical Boundary

InfoDashboard generation does not automatically reuse the OpenClaw agent's current model or API key.

The server resolves its own LLM provider and database credentials from `.env.local`. This skill does not rely on runtime overrides.

If the user wants to change any of those, they must edit `.env.local`.

## Interaction Policy

- Do not begin by asking the user to paste an API key or database password into chat.
- First, recommend an LLM provider path.
- Then guide the user to edit `.env.local` themselves.
- Do not offer to write secrets for them.
- If generation fails due to auth, provider, or database errors, direct the user back to `.env.local`.

## Setup Procedure

```bash
cp .env.example .env.local
```

Then edit `.env.local` with the values below.

## Required: LLM Provider (choose one)

### Option 1 — Anthropic (Recommended)

```env
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_MODEL=claude-sonnet-4-6
```

Why: Best instruction-following for code generation; avoids needing `OPENAI_BASE_URL`.

### Option 2 — OpenAI or Compatible (DeepSeek, Qwen, etc.)

```env
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1   # omit for official OpenAI
DEFAULT_MODEL=gpt-4o
```

Why: Use when the user already has an OpenAI-compatible key.

## Required: Database Connection via SOCKS5 Tunnel

InfoDashboard connects to a SQL Server inside a private network through an frp SOCKS5 tunnel.

```env
SOCKS5_HOST=127.0.0.1
SOCKS5_PORT=1080
SOCKS5_USER=                 # SOCKS5 proxy username (required if frp server enables auth)
SOCKS5_PASS=                 # SOCKS5 proxy password

DB_HOST=                     # SQL Server IP inside the private network
DB_PORT=1433
DB_USER=                     # SQL Server login name
DB_PASS=
DB_NAME=
```

### frpc Setup

`frpc-visitor.ini` is **not included** in the repo (it contains server IPs and tokens).
Copy the example and fill in the real values:

```bash
cp tools/frpc-visitor.ini.example tools/frpc-visitor.ini
# then edit tools/frpc-visitor.ini with the real server_addr, token, and sk
```

Binaries are included in `tools/`:

- Windows: `tools/frpc.exe`
- Linux: `tools/frpc-linux`

The frp tunnel is started **automatically** when `main.py` starts. No manual launch needed.
If the tunnel fails to connect, the server logs a warning and DB calls will fail.

## Optional: Deployment Port Range

```env
DASHBOARD_PORT_START=8501
DASHBOARD_PORT_END=8600
```

Defaults are fine for most users. Only change if those ports are already in use.

## Confirmation Requirements

- Recommend one LLM provider path first.
- Tell the user exactly which variables to edit in `.env.local`.
- Ask the user to confirm frpc is running before continuing.
- Wait for the user to confirm they finished editing before continuing.
- Do not request the literal key or password in chat.
