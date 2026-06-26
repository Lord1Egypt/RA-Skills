<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors

This INSTALL.md is MIT-0-licensed. Targets NousResearch Hermes Agent
v0.12 or later. Underlying InvestorClaw service is Apache 2.0.
-->

# Install — InvestorClaw v4.0 for Hermes Agent (v0.12+)

This is a five-step install. Total wall time ~5 minutes on a warm
Docker host (longer on first pull while images come down).

## Prerequisites

- **Hermes Agent v0.12 or later.** Check with `hermes --version`.
  Earlier versions used a different skill-injection model (see HER-1
  in v2.x release notes) and are not compatible with the v4.0
  MCP-HTTP architecture.
- **Docker** (or **Podman** with `docker compose` shim) available on
  the host. Verify with `docker --version` and
  `docker compose version`.
- **`curl`** (for staging the compose file).
- Free local ports **8090** (ic-engine MCP), **5002** (mnemos MCP),
  **8092** (dashboard).

---

## Step 1 — Drop this skill into hermes

Copy this directory into hermes' skill path:

```bash
mkdir -p ~/.hermes/skills/investorclaw
cp -R /path/to/agent-skills/hermes/. ~/.hermes/skills/investorclaw/
```

After the copy, `~/.hermes/skills/investorclaw/` should contain
`SKILL.md`, `DESCRIPTION.md`, `INSTALL.md`, and
`config-snippet.yaml`. Hermes 0.12+ uses `DESCRIPTION.md` for the
short catalog entry (`skills_list`) and `SKILL.md` for the long
view (`skill_view`).

---

## Step 2 — Install the InvestorClaw service

The service is two containers in a single compose file:

```bash
mkdir -p ~/.investorclaw
curl -sSL https://raw.githubusercontent.com/ncz-os/mnemos-ic-runtime/main/compose.yml \
  > ~/.investorclaw/compose.yml
cd ~/.investorclaw && docker compose up -d
```

Wait for both containers to report healthy:

```bash
curl -fsS http://localhost:18090/healthz   # ic-engine
curl -fsS http://localhost:5002/healthz   # mnemos-rs
```

Both should return 200 with a JSON body. First pull may take a few
minutes while images download.

---

## Step 3 — Add MCP servers to `~/.hermes/config.yaml`

Open `~/.hermes/config.yaml` and merge in the contents of
`config-snippet.yaml` (in this directory). The block to add:

```yaml
mcp_servers:
  investorclaw:
    transport: http
    url: http://localhost:18090/mcp
  mnemos:
    transport: http
    url: http://localhost:5002/mcp
```

If you already have an `mcp_servers:` block, add the two new keys
under it — do NOT replace the whole block. YAML merging is
key-by-key, so just paste the two server entries inside your
existing `mcp_servers:` map.

---

## Step 4 — Restart hermes

Hermes only handshakes with MCP servers at startup. Restart so it
picks up the new config:

```bash
# If running as a one-shot CLI, just invoke a fresh `hermes chat ...`.
# If running as a daemon / service, restart that:
hermes daemon restart   # if you use the daemon mode
# or kill -HUP <pid>    # depending on your setup
```

Verify hermes sees the new servers:

```bash
hermes mcp list
# Expected: investorclaw  http  http://localhost:18090/mcp  connected
#           mnemos        http  http://localhost:5002/mcp  connected
```

(If your hermes build doesn't have `hermes mcp list`, the tools
will still appear in the catalog at chat time — try Step 5.)

---

## Step 5 — Try it

```bash
hermes chat -q "What is in my portfolio?" \
  --provider gemini -m gemini-2.5-flash --yolo
```

(Substitute your preferred provider / model — Together /
MiniMaxAI/MiniMax-M2.7, OpenAI / gpt-4.5, etc.)

Then open the dashboard at <http://localhost:18092> to:

- Upload a broker CSV / XLS / PDF.
- Configure provider API keys (if the service should call out to
  any external APIs for news, prices, etc.).
- Map columns if your broker file has a non-standard header.

After the first portfolio is uploaded, ask follow-ups like
"What's my Sharpe ratio?" or "What's the worst performer this
month?" — hermes will route those to the appropriate `investorclaw.*`
tool natively.

---

## Troubleshooting

**Tools not appearing in hermes' catalog.**
1. Confirm `~/.hermes/config.yaml` is valid YAML —
   `python3 -c "import yaml; yaml.safe_load(open('$HOME/.hermes/config.yaml'))"`.
2. Confirm hermes was restarted after editing config.
3. Run `hermes mcp list` — if it lists the servers as
   `disconnected`, the service isn't reachable.
4. Confirm the service is up:
   `docker ps | grep -E 'ic-engine|mnemos'` should show two
   `Up` rows. If not, `cd ~/.investorclaw && docker compose up -d`.
5. Confirm health: `curl -fsS http://localhost:18090/healthz` and
   `curl -fsS http://localhost:5002/healthz` both 200.

**Tools appear but `portfolio_ask` returns "no portfolio loaded".**
Open <http://localhost:18092>, upload a broker CSV / XLS / PDF, then
re-ask. The dashboard's column-mapping wizard handles non-standard
broker formats.

**Ports already in use.** Edit `~/.investorclaw/compose.yml` to
remap the host-side port (the container side stays at 8090 / 5002 /
8092), then update `config-snippet.yaml` and `~/.hermes/config.yaml`
to match.

**Reverting to v2.x.** Don't. v2.x carries the HER-1 caveat
(skill-as-doc-hint, ~8% reliability on hermes). v4.0's MCP-HTTP
architecture is the supported path.
