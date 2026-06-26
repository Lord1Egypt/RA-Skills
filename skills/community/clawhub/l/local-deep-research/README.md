# Local Deep Research (LDR) — OpenClaw Skill

> Multi-cycle deep research using a **locally-hosted** Local Deep Research (LDR) service for OpenClaw / ClawHub. Use this skill when you need comprehensive research with citations, literature reviews, competitive intelligence, or exhaustive web search with iterative question generation.

**Triggers:** "deep research", "research this topic", "comprehensive analysis with sources", "literature review", "investigate [topic]", or when local LDR is preferred over cloud research.

---

## Before installing

- **Required**: `curl` and `jq` must be installed. The skill declares these in its manifest (`requires.bins`).
- **Environment / credentials**: The skill expects `LDR_BASE_URL` (default `http://127.0.0.1:5000`) and, if your LDR uses auth, `LDR_SERVICE_USER` and `LDR_SERVICE_PASSWORD` (or `LDR_USERNAME`/`LDR_PASSWORD`). These are declared in the skill manifest (`requires.env` / `primaryEnv`). Set them via your environment or a local `.env` file only; do not commit secrets.
- **Trust**: Only point `LDR_BASE_URL` at an LDR instance you control (e.g. localhost). The script sources `~/.config/local_deep_research/config/.env` if present—verify that file’s contents and do not put unrelated secrets there.
- **Optional**: Review `scripts/ldr-research.sh`; for higher assurance, run the skill in an isolated environment with network restricted to your LDR host.

---

## Requirements

- A running **LDR** instance (e.g. `http://127.0.0.1:5000`)
- OpenClaw with network and shell permissions
- `curl` and `jq` on the host
- (If LDR has auth enabled) LDR account credentials — **stored only locally**, see below

---

## Quick start

1. **Install the skill** (e.g. via ClawHub or copy into your OpenClaw skills directory).
2. **Set LDR URL** (optional if using default):
   ```bash
   export LDR_BASE_URL="http://127.0.0.1:5000"
   ```
3. **If your LDR instance requires login**, set credentials via **environment variables or a local `.env` file only** (see [Credentials](#credentials-local-only)):
   ```bash
   export LDR_SERVICE_USER="your-ldr-username"
   export LDR_SERVICE_PASSWORD="your-ldr-password"
   ```
4. Run research via the skill (e.g. "Research the latest developments in quantum computing").

---

## Credentials (local-only)

LDR uses **session-cookie authentication with CSRF protection** (not HTTP Basic Auth). The script performs a proper login flow: fetches the login page for a session cookie and CSRF token, then POSTs the login form. Your username and password are used **only** to create that session with **your local** LDR instance (and for LDR’s per-user encrypted results).

- **They are not transmitted** to any third party or to ClawHub/GitHub — only to your own LDR instance (e.g. on localhost).
- **Do not** put credentials in the skill config file or commit them to git.

### Recommended: environment variables or LDR’s `.env`

- **Option A — Environment variables**  
  In your shell or process:
  ```bash
  export LDR_SERVICE_USER="openclaw_service"
  export LDR_SERVICE_PASSWORD="a-strong-password"
  ```
- **Option B — LDR config directory**  
  LDR can load `~/.config/local_deep_research/config/.env`. This script will source that file if it exists, so you can keep one local file for LDR and this skill. Ensure that path is **not** in git (e.g. in `.gitignore` if you ever copy it into a project).
- **Option C — Project `.env`**  
  If you use a project-level `.env`, add it to `.gitignore` and never commit it.

Use a **dedicated LDR user** (e.g. `openclaw_service`) for this skill so you can rotate that account without affecting your personal LDR login.

See `env.example` for variable names. Do **not** commit real credentials.

---

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `LDR_BASE_URL` | LDR service URL | `http://127.0.0.1:5000` |
| `LDR_LOGIN_URL` | Login page URL (session + CSRF) | `$LDR_BASE_URL/auth/login` |
| `LDR_SERVICE_USER` | LDR account username (local auth only) | — |
| `LDR_SERVICE_PASSWORD` | LDR account password (local auth only) | — |
| `LDR_CONFIG_DIR` | Directory containing `.env` to source | `~/.config/local_deep_research/config` |
| `LDR_DEFAULT_MODE` | Research mode: `quick` (Quick Summary) or `detailed` (Detailed Report) | `detailed` |
| `LDR_DEFAULT_LANGUAGE` | Default output language for report/summary (e.g. `en`, `es`, `fr`, `de`, `zh`, `ja`) | — |
| `LDR_DEFAULT_SEARCH_TOOL` | Search tool: `searxng`, `auto`, `local_all` | `auto` |

**Research modes:** Use `quick` for a short summary (faster); use `detailed` for a full report with full citations. You can override the output language per run with `--language` (e.g. `--language es` for Spanish).

`LDR_USERNAME` / `LDR_PASSWORD` are supported as fallbacks.

---

## Actions

The skill exposes these actions via `scripts/ldr-research.sh`:

| Action | Description |
|--------|-------------|
| `start_research` | Submit a query; returns `research_id`. |
| `get_status` | Check job status by `research_id`. |
| `get_result` | Fetch the full report when completed. |
| `poll_until_complete` | Block until the job completes or times out. |

See **SKILL.md** for input/output schemas and orchestration patterns.

---

## Project layout

```
local-deep-research/
├── README.md           # This file
├── SKILL.md            # OpenClaw skill instructions (entry point)
├── env.example         # Example env vars (no secrets)
├── references/
│   ├── api.md          # LDR API reference
│   └── examples.md     # Usage examples
└── scripts/
    └── ldr-research.sh # CLI for start_research, get_status, get_result, poll_until_complete
```

---

## Troubleshooting

- **LDR not responding**  
  Check `LDR_BASE_URL` and that LDR is running: `curl "$LDR_BASE_URL/health"`.

- **Authentication failures**  
  LDR uses **session + CSRF**, not Basic Auth. Ensure `LDR_SERVICE_USER` and `LDR_SERVICE_PASSWORD` (or `LDR_USERNAME`/`LDR_PASSWORD`) are set via env or a local `.env` that is **not** committed. Run the script and look for "Login successful"; or open `LDR_LOGIN_URL` in a browser to confirm LDR’s login page works.

- **Research stuck**  
  Check LDR logs and service health; consider timeout/restart if there’s no progress for a long time.

---

## Publishing (ClawHub / GitHub)

- **ClawHub:** From the skill root, run  
  `clawhub publish . --slug local-deep-research --name "Local Deep Research" --version 1.0.0 --tags latest`  
  (Requires `clawhub login` first.)
- **GitHub:** Ensure `.gitignore` is in place so `.env` and secrets are never committed. Clone or fork the repo as usual.

## License

MIT — see [LICENSE](LICENSE).

## Links

- [ClawHub](https://clawhub.ai/) — OpenClaw skill registry  
- [OpenClaw](https://docs.openclaw.ai/) — Documentation

## Author

[Edward Tsang](https://github.com/eplt) — blockchain & AI engineer. Open to consulting → [Email](mailto:edward@odw.ai) · [LinkedIn](https://www.linkedin.com/in/edwardtsang/)
