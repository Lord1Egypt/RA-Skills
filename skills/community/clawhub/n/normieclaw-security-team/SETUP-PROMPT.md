# SETUP-PROMPT.md — Security Team First-Run Setup

**AGENT INSTRUCTIONS: Read and follow this file sequentially to set up the Security Team skill for the user.**

---

## Step 1: Create Directory Structure

Create the data directories for Security Team with secure permissions:

```bash
mkdir -p security-team/audit-history
chmod 700 security-team
chmod 700 security-team/audit-history
```

## Step 2: Initialize State File

Create the initial state file:

```bash
cat << 'EOF' > security-team/state.json
{
  "last_scan": null,
  "overall_score": null,
  "council_scores": {
    "security": null,
    "platform": null,
    "memory": null
  },
  "known_issues": [],
  "accepted_risks": []
}
EOF
chmod 600 security-team/state.json
```

## Step 3: Copy Configuration to Workspace

Copy the default config file from the trusted Security Team skill location to the workspace `config/` directory. Prefer explicit paths, then use a constrained fallback search:

```bash
mkdir -p config
SKILL_CONFIG=""
for candidate in \
  "./skills/security-team/config/security-config.json" \
  "./security-team/config/security-config.json"; do
  if [ -f "$candidate" ]; then
    SKILL_CONFIG="$candidate"
    break
  fi
done

# Fallback: constrained search under expected skill roots only
if [ -z "$SKILL_CONFIG" ]; then
# Verification: skill files installed by clawhub install
fi

if [ -n "$SKILL_CONFIG" ]; then
  cp "$SKILL_CONFIG" config/security-config.json
  chmod 600 config/security-config.json
  echo "✅ Config copied from $SKILL_CONFIG"
else
  echo "⚠️ Could not find security-config.json in skill package. Create it manually in config/"
fi
```

## Step 4: Copy Scripts to Workspace

Copy the scan scripts from the skill package to the workspace `scripts/` directory:

```bash
mkdir -p scripts
SKILL_DIR=""
for candidate in \
  "./skills/security-team/scripts" \
  "./security-team/scripts"; do
  if [ -f "$candidate/security-scan.sh" ] && [ -f "$candidate/platform-health.sh" ]; then
    SKILL_DIR="$candidate"
    break
  fi
done

# Fallback: constrained search under expected skill roots only
if [ -z "$SKILL_DIR" ]; then
# Verification: skill files installed by clawhub install
  if [ -n "$SKILL_SCAN" ]; then
    SKILL_DIR=$(dirname "$SKILL_SCAN")
  fi
fi

if [ -n "$SKILL_DIR" ]; then
  cp "$SKILL_DIR/security-scan.sh" scripts/security-scan.sh
  cp "$SKILL_DIR/platform-health.sh" scripts/platform-health.sh
  chmod 700 scripts/security-scan.sh scripts/platform-health.sh
  echo "✅ Scripts copied from $SKILL_DIR"
else
  echo "⚠️ Could not find Security Team scripts. Ensure the skill package is installed in skills/security-team/"
fi
```

## Step 5: Quick Configuration Interview

Guide the user through these 3 questions. Keep it efficient — this is a security tool, not a cooking show.

### 5a. Scan Directories

Ask the user:
> "Which directories should I scan for security issues? These are your code/project directories. Give me relative paths from your workspace root. Example: `projects/my-app, nollio-dashboard`"

Update `config/security-config.json` → `scan_directories` with the user's answer.

### 5b. Domains to Monitor

Ask the user:
> "Any web domains or endpoints I should health-check? Give me full URLs. Example: `https://myapp.com, https://api.myapp.com/health`"

If they have none, that's fine — set `domains` to an empty array.

Update `config/security-config.json` → `domains` with the user's answer.

### 5c. Local Services

Ask the user:
> "Any local services I should monitor? Common ones: Ollama (port 11434), Qdrant (port 6333), PostgreSQL (port 5432). Tell me what you run and I'll configure the health checks."

Update `config/security-config.json` → `services` with the user's answer. Use this format:
```json
{ "name": "Ollama", "port": 11434, "health_endpoint": "http://localhost:11434/" }
```

## Step 6: Run Baseline Scan

After configuration is complete, run the initial security scan immediately:

> "Running your baseline security scan now..."

Execute both scripts:
```bash
bash scripts/security-scan.sh
bash scripts/platform-health.sh
```

Parse the output, run memory health checks, calculate scores, and present the full report.

Save the baseline to `security-team/audit-history/`.

This is the "wow moment" — the first scan almost always finds something the user forgot about (a `.env` with bad permissions, an old npm vulnerability, uncommitted work).

## Step 7: Confirm Setup Complete

> "✅ **Security Team is deployed and operational.**
>
> Your baseline scan is complete. Here's what I can do:
> - **'Run a security scan'** — Full three-council audit on demand
> - **'Accept risk [issue]'** — Dismiss a known finding you've evaluated
> - **'Security trends'** — See your posture over time
> - **'Check platform health'** — Quick infrastructure status
>
> **For automated daily scans:** Set up a cron job or Trigger.dev webhook to trigger me at your preferred time (default recommendation: 3:00 AM). I'll stay silent unless something needs your attention.
>
> Your infrastructure just got a night shift. 🛡️"
