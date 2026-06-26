# Imperial Orchestrator

[中文](../README.md) | **[English](./README.en.md)** | [日本語](./README.ja.md) | [한국어](./README.ko.md) | [Español](./README.es.md) | [Français](./README.fr.md) | [Deutsch](./README.de.md)

---

OpenClaw High-Availability Multi-Role Model Orchestration Skill — Intelligent routing inspired by the ancient Chinese "Three Departments and Six Ministries" court system.

> **Design Inspiration**: The role architecture draws from the [Three Departments and Six Ministries (三省六部)](https://github.com/cft0808/edict) imperial court governance pattern, combined with deep AI prompt engineering techniques from [PUA](https://github.com/tanweai/pua).

## Core Capabilities

- **Three Departments & Six Ministries** role orchestration: 10 roles, each with clear responsibilities
- **Auto-Discovery** of 46+ models from openclaw.json
- **Intelligent Routing** by domain (coding / ops / security / writing / legal / finance)
- **Opus Priority** for coding/security/legal tasks — strongest model first
- **Cross-Provider Failover** auth circuit-breaker → cross-vendor degradation → local survival
- **Real Execution** API calls + token counting + cost tracking
- **Benchmarking** same task across all models, scored and ranked
- **Multi-Language** support for 7 languages: zh/en/ja/ko/es/fr/de

## Quick Start

```bash
# 1. Discover models
python3 scripts/health_check.py --openclaw-config ~/.openclaw/openclaw.json --write-state .imperial_state.json

# 2. Validate models
python3 scripts/model_validator.py --openclaw-config ~/.openclaw/openclaw.json --state-file .imperial_state.json

# 3. Route a task
python3 scripts/router.py --task "Write a concurrent-safe LRU Cache in Go" --state-file .imperial_state.json

# All-in-one
bash scripts/route_and_update.sh full "Fix WireGuard peer sync bug"
```

## Role System: Three Departments & Six Ministries

Each role is equipped with a deep system prompt covering identity, responsibilities, behavioral rules, collaboration awareness, and red lines.

### Central Hub

| Role | Title | Court Equivalent | Core Mission |
|------|-------|-----------------|--------------|
| **router-chief** | Chief Router | Emperor / Central Bureau | System lifeline — classify, route, maintain heartbeat |

### Three Departments

| Role | Title | Court Equivalent | Core Mission |
|------|-------|-----------------|--------------|
| **cabinet-planner** | Chief Strategist | Secretariat (中书省) | Draft strategies — decompose chaos into ordered steps |
| **censor-review** | Chief Censor | Chancellery (门下省) | Review and veto — the final quality gatekeeper |

### Six Ministries

| Role | Title | Court Equivalent | Core Mission |
|------|-------|-----------------|--------------|
| **ministry-coding** | Minister of Engineering | Ministry of Works | Build and construct — coding, debugging, architecture |
| **ministry-ops** | Deputy Minister of Infrastructure | Ministry of Works · Construction Bureau | Maintain roads — deployment, ops, CI/CD |
| **ministry-security** | Minister of Defense | Ministry of War | Guard the borders — security audit, threat modeling |
| **ministry-writing** | Minister of Culture | Ministry of Rites | Culture and etiquette — copywriting, docs, translation |
| **ministry-legal** | Minister of Justice | Ministry of Justice | Law and order — contracts, compliance, terms |
| **ministry-finance** | Minister of Revenue | Ministry of Revenue | Taxation and treasury — pricing, margin, settlement |

### Emergency Courier

| Role | Title | Court Equivalent | Core Mission |
|------|-------|-----------------|--------------|
| **emergency-scribe** | Emergency Courier | Express Courier Station | Last resort to keep the system alive |

## Operating Rules

1. **401 Circuit Breaker** — auth failure immediately marks `auth_dead`, cools the entire auth chain, cross-provider switch takes priority
2. **Keep Router Lightweight** — don't assign the heaviest prompts or most fragile providers to router-chief
3. **Cross-Provider First** — fallback order: same role different provider → local model → adjacent role → emergency courier
4. **Degrade, Never Crash** — even if all top models fail, respond with architecture advice, checklists, pseudocode

## Routing Output

```json
{
  "mode": "plan_then_execute",
  "mode_labels": {"zh": "先规划后执行", "en": "Plan then Execute", "ja": "計画後実行"},
  "lead_role": "ministry-coding",
  "lead_title": "Minister of Engineering",
  "lead_titles": {"zh": "工部尚书", "en": "Minister of Engineering", "ja": "工部尚書"},
  "selected_model": "cliproxy/claude-opus-4-6",
  "fallback_chain": ["ollama/qwen3.5:27b", "cliproxy/gpt-5.1-codex"],
  "survival_model": "ollama/gpt-oss:20b"
}
```

## Project Structure

```
config/
  agent_roles.yaml          # Role definitions (responsibilities, capabilities, fallback chains)
  agent_prompts.yaml        # Deep system prompts (identity, rules, red lines)
  routing_rules.yaml        # Routing keyword rules
  failure_policies.yaml     # Circuit breaker / retry / degradation policies
  benchmark_tasks.yaml      # Benchmark task library
  model_registry.yaml       # Model capability overrides
  i18n.yaml                 # 7-language adaptation
scripts/
  lib.py                    # Core library (discovery, classification, state management, i18n)
  router.py                 # Router (role matching + model selection)
  executor.py               # Execution engine (API calls + fallback)
  orchestrator.py           # Full pipeline (route → execute → review)
  health_check.py           # Model discovery
  model_validator.py        # Model probing
  benchmark.py              # Benchmark + leaderboard
  route_and_update.sh       # Unified CLI entry point
```

## Installation

### Prerequisites: Install OpenClaw

```bash
# 1. Install OpenClaw CLI (macOS)
brew tap openclaw/tap
brew install openclaw

# Or install via npm
npm install -g @openclaw/cli

# 2. Initialize configuration
openclaw init

# 3. Configure model providers (edit ~/.openclaw/openclaw.json)
openclaw config edit
```

> For detailed installation docs, see the [OpenClaw official repository](https://github.com/openclaw/openclaw)

### Install Imperial Orchestrator Skill

```bash
# Option 1: Clone from GitHub
git clone https://github.com/rexnode/imperial-orchestrator.git
cp -r imperial-orchestrator ~/.openclaw/skills/

# Option 2: Copy directly to global skills directory
cp -r imperial-orchestrator ~/.openclaw/skills/

# Option 3: Workspace-level install
cp -r imperial-orchestrator <your-workspace>/skills/
```

### Verify Installation

```bash
# Discover and probe models
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/health_check.py \
  --openclaw-config ~/.openclaw/openclaw.json \
  --write-state .imperial_state.json

# Verify routing works
python3 ~/.openclaw/skills/imperial-orchestrator/scripts/router.py \
  --task "Write a Hello World" \
  --state-file .imperial_state.json
```

## Security

- Never send secrets in prompts
- Keep probe requests minimal
- Manage provider health separately from model quality
- A model appearing in config does not mean it is safe to route

## License

MIT
