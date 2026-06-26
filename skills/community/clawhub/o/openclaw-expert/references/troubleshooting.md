# Troubleshooting — Häufige Probleme & Lösungen

## Diagnose-Grundlagen

```bash
# IMMER zuerst:
openclaw --version
openclaw doctor
openclaw doctor --run doctor    # DM-Policy-Check
openclaw doctor --run security  # Security-Audit
openclaw status

# Logs lesen:
journalctl --user -u openclaw-gateway -n 50 --no-pager
# oder:
tail -n 120 /tmp/openclaw-gateway.log
# Docker:
docker compose logs -f openclaw-gateway

# Deep Health (Gateway + Channels):
openclaw health --token "$OPENCLAW_GATEWAY_TOKEN"
```

---

## Gateway startet nicht nach Config-Änderung

```bash
# 1. Config validieren
openclaw doctor

# 2. JSON5-Syntax prüfen
node -e "require('fs').readFileSync(process.env.HOME+'/.openclaw/openclaw.json','utf8')" && echo "OK"

# 3. Logs analysieren
journalctl --user -u openclaw-gateway -n 50 --no-pager
tail -n 120 /tmp/openclaw-gateway.log

# 4. Port belegt?
ss -ltnp | grep 18789

# 5. Backup wiederherstellen
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
systemctl --user restart openclaw-gateway
```

**Häufigste Ursache**: Unbekannter Key oder falscher Typ in openclaw.json.
JSON5 erlaubt Kommentare, aber keine unbekannten Felder!

---

## "systemctl --user unavailable"

```bash
# Falsch: Als root eingeloggt
# Richtig: Als openclaw-User einloggen
ssh openclaw@<server-ip>

# Dann:
openclaw gateway install
systemctl --user start openclaw-gateway
systemctl --user enable openclaw-gateway

# Wenn lingering fehlt:
loginctl enable-linger openclaw
```

---

## Modell hinzufügen schlägt fehl

```bash
# Fallstricke:
# 1. "id" muss "provider/model-name" Format haben
# 2. Bei OpenRouter-Style IDs: Provider-Prefix dazu!
#    z.B. "openrouter/moonshotai/kimi-k2"
# 3. "api": "openai-completions" vs "openai-responses" (versionsabhängig!)
# 4. "contextWindow" und "maxTokens" müssen Zahlen sein, keine Strings!
# 5. Ollama in Docker: baseUrl = "http://host.docker.internal:11434"
```

---

## Node verbindet nicht

```bash
openclaw nodes status
openclaw channels status --probe

# Gateway muss von Node erreichbar sein:
# - Tailscale: gateway.bind auf "tailscale" setzen
# - Lokales Netz: gateway.bind auf "lan" (nur mit VPN!)
# - Port 18789 muss erreichbar sein
```

---

## Skills werden nicht geladen

```bash
# Skills erst in neuer Session aktiv!
openclaw gateway restart

# Dann prüfen:
openclaw skills list

# Skill-Verzeichnisse prüfen:
ls ~/.openclaw/workspace/skills/    # Workspace-Skills
ls ~/.openclaw/skills/              # Managed-Skills

# Nur 1 von N Skills sichtbar?
# → SKILL.md prüfen:
#   - YAML-Frontmatter mit name + description?
#   - Kein Syntax-Fehler im YAML?
#   - Doppelpunkte in description mit Quotes escapen!
```

---

## Heartbeat-Probleme

### Heartbeat-Model-Bug (Issue #22133)
```
Symptom: Main-Session plötzlich mit 16k Context statt 200k
Ursache: heartbeat.model überschreibt main-Session-Model
Fix: heartbeat.model entfernen oder auf gleiches Model setzen
Workaround: /new in Telegram → Modell wird zurückgesetzt
```

### Heartbeat verbraucht zu viele Tokens
```json5
agent: {
  heartbeat: {
    every: "6h",       // Von "30m" auf "6h" reduzieren
    // oder:
    every: "off",      // Heartbeat komplett deaktivieren
  },
}
```

---

## Memory-Probleme

### Memory wird nicht gefunden
```bash
# memorySearch aktiv?
openclaw config get agents.defaults.memorySearch.enabled

# Embedding-Provider konfiguriert?
# Auto-Detect: local → openai → gemini
# Manuell prüfen: API-Key für Embeddings vorhanden?

# Erster Aufruf langsam → QMD lädt GGUF-Modelle herunter
```

### Memory geht bei Compaction verloren
```json5
// memoryFlush aktivieren:
agents: {
  defaults: {
    compaction: {
      memoryFlush: { enabled: true },
    },
  },
}
```

### MEMORY.md wird in Gruppen geladen (Datenschutz!)
→ Das sollte NICHT passieren. MEMORY.md wird nur in privaten Sessions geladen.
Falls doch: `openclaw doctor` + Version updaten.

---

## WhatsApp-Probleme

| Problem | Lösung |
|---|---|
| QR-Code abgelaufen | `openclaw channels login` erneut |
| Bot antwortet nicht | `openclaw channels status --probe` |
| Fremde können schreiben | `dmPolicy: "allowlist"` + `allowFrom` prüfen |
| Bot in Gruppen zu geschwätzig | Gruppen-Verhalten in AGENTS.md regeln |

---

## Performance-Probleme

| Problem | Lösung |
|---|---|
| Langsame Antworten | Model-Latenz prüfen, ggf. kleineres Model |
| Hohe Kosten | Heartbeat-Intervall erhöhen, günstigeres Model |
| Docker langsam auf macOS | npm-Installation statt Docker nutzen |
| Context-Compaction zu häufig | Größeres Model-Context-Window nutzen |
| Memory-Search langsam | Erster Aufruf = Model-Download, danach schneller |

---

## Notfall: Komplett zurücksetzen

```bash
# 1. Gateway stoppen
systemctl --user stop openclaw-gateway

# 2. Backup (!)
tar czf ~/openclaw-emergency-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/

# 3. Config zurücksetzen
openclaw onboard    # Wizard erneut durchlaufen

# 4. Oder: Backup-Config wiederherstellen
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json

# 5. Neu starten
systemctl --user start openclaw-gateway
openclaw doctor
```

---

## SecretRef-Probleme

### "Secret provider not found"

```bash
# Provider-Config prüfen:
openclaw secrets configure --providers-only

# Testen:
openclaw secrets reload

# Audit:
openclaw secrets audit --check
```

**Häufige Ursachen:**
- Fehlender `secrets.providers` Block in Config
- `provider`-Name nicht registriert
- `exec`-Kommando nicht ausführbar

### "Environment variable not found"

```json5
// Falsch:
{ source: "env", provider: "default", id: "openai_api_key" }  // Kleinbuchstaben

// Richtig:
{ source: "env", provider: "default", id: "OPENAI_API_KEY" }  // GROSSBUCHSTABEN
```

### Exec-SecretRef mit 1Password

```json5
secrets: {
  providers: {
    onepassword: {
      source: "exec",
      command: "/opt/homebrew/bin/op",
      args: ["read", "op://Vault/Item/field"],
      allowSymlinkCommand: true,  // Für Homebrew-Shims
    },
  },
}
```

---

## Sandbox-Probleme

### Container startet nicht

```bash
# Image prüfen:
docker images | grep openclaw-sandbox

# Fehlt? Nachbauen:
scripts/sandbox-setup.sh  # Standard
scripts/sandbox-common-setup.sh  # Mit Tooling
```

### Permission denied in Sandbox

```bash
# UID/GID mismatch
# Option 1: Container-User auf Host-User setzen
docker.user: "1000:1000"

# Option 2: Workspace beschreibbar
sudo chown -R 1000:$(id -g) ~/.openclaw/workspace
```

### Tools nicht gefunden in Sandbox

```json5
// setupCommand braucht Netzwerk + Root:
sandbox: {
  docker: {
    network: "bridge",      // Nicht "none"!
    readOnlyRoot: false,    // Für apt-get
    user: "0:0",            // Root für setup
    setupCommand: "apt-get update && apt-get install -y git curl jq",
  },
}
```

### Sandbox-Pod läuft nicht

```bash
# Status prüfen:
openclaw sandbox list
openclaw sandbox status

# Logs:
journalctl --user -u openclaw-gateway -n 100 | grep -i sandbox
```

---

## Skill-Gating-Probleme

### Skill wird nicht geladen

```bash
# Skill-Status prüfen:
openclaw skills list

# Wenn fehlt, SKILL.md prüfen:
# - YAML-Frontmatter mit name + description?
# - Kein Syntax-Fehler im YAML?
# - description darf KEINE Doppelpunkte ohne Quotes haben!
```

**YAML-Fehler-Beispiel:**
```markdown
# FALSCH:
---
name: my-skill
description: Use when X, Y: Z  ← Doppelpunkt ohne Quotes!
---

# RICHTIG:
---
name: my-skill
description: "Use when X, Y: Z"
---
```

### "requires.bins" nicht erfüllt

```json5
// Skill braucht Binary auf HOST und in Sandbox:
// 1. Host-Check: Binary auf PATH?
which uv

// 2. Sandbox: In setupCommand installieren
sandbox: {
  docker: {
    network: "bridge",
    readOnlyRoot: false,
    user: "0:0",
    setupCommand: "apt-get update && apt-get install -y curl && curl -LsSf https://astral.sh/uv/install.sh | sh",
  },
}
```

---

## Multi-Agent-Probleme

### Bindings greifen nicht

```bash
# Bindings auflisten:
openclaw agents list --bindings

# Häufige Fehler:
# - accountId vergessen (Default-Account wird angenommen)
# - peer-Format falsch (Channel-spezifisch)
# - Reihenfolge: Spezifische Bindings zuerst!
```

### Agent wird nicht gefunden

```json5
// Falsch: Kein default-Agent
agents: { list: [{ id: "work", ... }] }

// Richtig: Default-Agent markieren
agents: { list: [{ id: "main", default: true, ... }, { id: "work", ... }] }
```

### Credentials teilen

**Auth-Profile sind per-Agent!**

```bash
# Credential kopieren (manuell):
cp ~/.openclaw/credentials/anthropic/default \
   ~/.openclaw/agents/work/agent/credentials/anthropic/default
```

---

## Model-Provider-Probleme

### "Model not found"

```json5
// Falsches Format:
models: { default: "claude-sonnet-4" }  // Fehlt Provider!

// Richtig:
models: { default: "anthropic/claude-sonnet-4-20250514" }

// OpenRouter mit Provider-Prefix:
models: {
  providers: {
    openrouter: { baseUrl: "https://openrouter.ai/api", api: "openai-completions" },
  },
  default: "openrouter/anthropic/claude-sonnet-4",  // Provider-Prefix!
}
```

### Ollama in Docker

```json5
models: {
  providers: {
    ollama: {
      // macOS Docker Desktop:
      baseUrl: "http://host.docker.internal:11434",
      // Linux:
      // baseUrl: "http://172.17.0.1:11434",
      api: "openai-completions",
    },
  },
}
```

---

## Docker-Specific

### Build OOM (Exit 137)

```bash
# Mindestens 2GB RAM für Build
# Option 1: Swap erhöhen
# Option 2: Mit mehr RAM bauen
```

### Container nicht erreichbar

```bash
# Bind-Adresse prüfen:
docker compose exec openclaw-gateway env | grep BIND

# LAN-Access:
# gateway.bind: "lan" in docker-compose.yml oder OPENCLAW_GATEWAY_BIND=lan
```

### QR nicht angezeigt

```bash
# Dashboard → Channels → WhatsApp QR
# ODER:
openclaw channels login --channel whatsapp --qr terminal
```

---

## Performance-Optimierung

| Problem | Lösung |
|---------|--------|
| Langsame Antworten | Kleineres Model für heartbeat |
| Hohe API-Kosten | `heartbeat.every: "6h"` statt `"30m"` |
| Docker langsam auf macOS | npm-Installation statt Docker |
| Context-Compaction-Loop | Größeres contextWindow oder `compaction.maxTokens` erhöhen |
| Memory-Search langsam | Erster Aufruf = Model-Download (~5min) |
| Skills-Token-Overhead | Unnötige Skills deaktivieren (`enabled: false`) |
