# Gmail Auto Draft Setup

## 0) 接入方必须先提供

- Gmail OAuth 客户端文件：`~/.config/gmail-auto-draft/google-client-secret.json`
- 目标 Gmail 账号（如应用在 Testing，需加入测试用户）
- 固定关键词查询（`--query` 或 `--query-file`）
- 业务画像（`agency_profile.txt`）
- 回复风格规则（`style_rules.txt`）
- 模型配置：
  - 本机 GMN：`OPENAI_BASE_URL` + `OPENAI_MODEL`
  - 或 OpenAI 官方：`OPENAI_API_KEY` + `OPENAI_MODEL`

> 关键词建议手工维护，不自动改写。

---

## 1) Create Google OAuth credentials

1. Open Google Cloud Console.
2. Create/select a project.
3. Enable `Gmail API`.
4. Create OAuth client credentials (`Desktop app` recommended).
5. Download JSON and save it to:
   - `~/.config/gmail-auto-draft/google-client-secret.json` (recommended)
   - or any path, then pass `--client-secret-file`

Recommended scopes:
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/gmail.compose`

## 2) Install Python dependencies

```bash
cd skills/gmail-auto-draft/scripts
python3 -m pip install -r requirements.txt
```

## 3) Configure model backend

### Option A (recommended): use local OpenClaw GMN endpoint

```bash
export OPENAI_BASE_URL="http://127.0.0.1:18789/v1"
export OPENAI_MODEL="openclaw:main"
```

Ensure endpoint is enabled once:

```bash
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
openclaw gateway restart
```

### Option B: use OpenAI directly

```bash
export OPENAI_API_KEY="your_openai_key"
export OPENAI_MODEL="gpt-4o-mini"
```

## 4) First run and OAuth authorization

Local browser mode:

```bash
./run_once.sh --auth-mode local --max-emails 3
```

Headless server mode:

```bash
./run_once.sh --auth-mode console --max-emails 3
```

Token is saved to:
- `~/.config/gmail-auto-draft/token.json` by default
- or path from `--token-file`

## 5) Validate output

The script prints JSON:
- `processed`: number of drafted emails
- `created_drafts`: message/thread/draft IDs
- `skipped`: skipped reasons
- `errors`: per-message errors

## 6) Run as monitor

```bash
./run_once.sh --poll-interval 60 --max-emails 5
```

This polls every 60 seconds and drafts replies continuously.
