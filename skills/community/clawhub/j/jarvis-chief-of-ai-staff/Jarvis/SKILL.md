---
name: jarvis-chief-of-ai-staff
description: Deploy Jarvis, your Chief of AI Staff, on OpenClaw. Optimized for Dell Pro Max GB10 (NVIDIA DGX Spark) edge devices. Use when setting up Jarvis, configuring an AI executive agent, deploying OpenClaw on GB10, initializing agent persona and memory, or building an always-on local AI assistant for business operations. Powered by Gignaati.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins:
        - bash
        - systemctl
        - docker
      anyBins:
        - ollama
        - lms
    os:
      - linux
    homepage: https://gignaati.com
    author: Yogesh Huja
    license: MIT
---

# Jarvis — Chief of AI Staff

> **Your always-on, local-first AI executive that runs entirely on-premise.**
> Zero cloud bills. Zero data egress. Full enterprise intelligence.

**Created by:** [Yogesh Huja](https://www.linkedin.com/in/yogeshhuja/) — Founder & CEO, [Gignaati](https://gignaati.com)
**Book:** [Invisible Enterprises](https://www.invisible-enterprises.com/) — Best-selling guide on leading with People & AI Agents

---

## What Is Jarvis?

Jarvis is not a chatbot. Jarvis is your **Chief of AI Staff** — a strategic, proactive, always-on AI executive that manages operations, communications, research, and project orchestration autonomously from your Dell Pro Max GB10 (NVIDIA DGX Spark).

Jarvis runs entirely on your hardware. No data leaves your machine. No API costs. No cloud dependency.

## Who Is This For?

- Founders, CEOs, and CTOs who want an AI-powered operations layer
- Enterprises deploying on-premise AI agents under DPDP Act or data sovereignty requirements
- Teams using Dell Pro Max GB10 or NVIDIA DGX Spark for edge AI
- Anyone building a production-grade OpenClaw agent beyond basic chat

## What Jarvis Can Do

- **Email & Calendar Secretary** — Inbox triage, scheduling, draft replies, meeting management
- **Proactive Project Management** — Status updates, follow-ups, sprint tracking via WhatsApp or messaging
- **Research Agent** — Web search combined with local files for personalized intelligence reports
- **Competitive Intelligence** — Monitor market shifts, competitor moves, technology trends
- **Sales Pipeline Support** — Draft outreach, track leads, generate proposals from templates
- **System Guardian** — Monitor GPU health, RAM, disk usage, and alert on anomalies

---

## Prerequisites

Before running Jarvis, ensure:

1. **Hardware:** Dell Pro Max GB10 (NVIDIA DGX Spark) running Linux (Ubuntu-based)
2. **OpenClaw:** Installed and onboarded (`openclaw --version` returns a valid version)
3. **LLM Backend:** Either Ollama or LM Studio installed and running
4. **Model:** At least one model pulled (recommended: `qwen3.5:35b-a3b` or `qwen3.5:27b`)
5. **Network:** Tailscale VPN configured for remote access (recommended, not required)
6. **Docker:** Installed for SearXNG web search (`docker --version`)

Verify readiness:

```bash
# Check all prerequisites
echo "=== Jarvis Readiness Check ==="
echo "OS: $(uname -srm)"
echo "OpenClaw: $(openclaw --version 2>/dev/null || echo 'NOT INSTALLED')"
echo "Ollama: $(ollama --version 2>/dev/null || echo 'NOT INSTALLED')"
echo "Docker: $(docker --version 2>/dev/null || echo 'NOT INSTALLED')"
echo "GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo 'NOT DETECTED')"
echo "Gateway: $(systemctl is-active openclaw 2>/dev/null || echo 'NOT RUNNING')"
echo "=== Check Complete ==="
```

---

## Installation

### Phase 1: Deploy Jarvis Persona (5 minutes)

This phase loads Jarvis's identity, memory, and operating instructions into your OpenClaw workspace.

**Step 1 — Back up your existing workspace:**

```bash
cp -r ~/.openclaw/workspace ~/.openclaw/workspace.backup.$(date +%Y%m%d) 2>/dev/null
echo "Backup complete (or no existing workspace found)."
```

**Step 2 — Deploy workspace files:**

```bash
bash {baseDir}/scripts/deploy-workspace.sh
```

This creates or updates the following files in `~/.openclaw/workspace/`:

| File | Purpose |
|------|---------|
| `SOUL.md` | Jarvis's behavioral philosophy, tone, and boundaries |
| `IDENTITY.md` | Name, role, voice, and presentation |
| `USER.md` | Your profile — edit this with your details |
| `MEMORY.md` | Curated long-term memory (Tier 1, always loaded) |
| `AGENTS.md` | Operating instructions, tool permissions, memory rules |
| `HEARTBEAT.md` | Proactive checklist for 30-minute heartbeat cycles |
| `TOOLS.md` | Local environment, installed skills, model-specific notes |
| `memory/` | Daily logs, people, projects, topics, decisions |

**Step 3 — Personalize USER.md:**

Open `~/.openclaw/workspace/USER.md` and replace placeholder values with your actual details:

```bash
nano ~/.openclaw/workspace/USER.md
```

Update: your name, email, company name, communication preferences, and priorities.

**Step 4 — Initialize git backup:**

```bash
cd ~/.openclaw/workspace
git init 2>/dev/null
git add -A
git commit -m "Jarvis workspace: initial deployment by gignaati/jarvis-chief-of-ai-staff"
```

### Phase 2: Configure LLM Backend (10 minutes)

**Option A — Ollama (recommended for simplicity):**

```bash
# Pull the recommended model
ollama pull qwen3.5:35b-a3b

# Verify it runs
ollama run qwen3.5:35b-a3b "Hello, I am Jarvis." --verbose
```

**Option B — LM Studio with llama.cpp (recommended for performance):**

For Qwen3.5-35B-A3B, you need the role translation proxy. See:
https://github.com/ZengboJamesWang/Qwen3.5-35B-A3B-openclaw-dgx-spark

**Configure OpenClaw to use local model:**

Edit `~/.openclaw/openclaw.json`:

```json
{
  "agent": {
    "model": "ollama/qwen3.5:35b-a3b",
    "workspace": "~/.openclaw/workspace",
    "thinkingDefault": "high",
    "timeoutSeconds": 1800,
    "heartbeat": {
      "every": "0m"
    }
  }
}
```

> **Note:** Start with heartbeat disabled (`"0m"`). Enable after you trust the setup.

### Phase 3: Enable Web Search (5 minutes)

**Option A — SearXNG (free, fully local, recommended):**

```bash
# Deploy SearXNG as a Docker container
docker run -d \
  --name searxng \
  --restart=always \
  -p 8888:8080 \
  -e SEARXNG_SECRET=$(openssl rand -hex 32) \
  searxng/searxng:latest

# Verify it works
sleep 5
curl -s "http://127.0.0.1:8888/search?q=test&format=json" | head -c 100
echo ""
echo "SearXNG is running at http://127.0.0.1:8888"
```

**Option B — Brave Search (built-in, costs $5/month):**

```bash
# Set your Brave API key
export BRAVE_API_KEY="BSA-your-key-here"
echo 'export BRAVE_API_KEY="BSA-your-key-here"' >> ~/.bashrc

# Configure in OpenClaw
openclaw configure --section web
```

### Phase 4: Security Hardening (5 minutes)

```bash
bash {baseDir}/scripts/security-harden.sh
```

This script:
- Configures WhatsApp allowlist (restricts who can message Jarvis)
- Enables sandbox mode for filesystem access
- Sets up UFW firewall rules
- Generates SSL certificates for the dashboard
- Creates a security audit log

### Phase 5: Verify Deployment (2 minutes)

**Restart the gateway:**

```bash
sudo systemctl restart openclaw
sleep 3
systemctl status openclaw
```

**Check that all workspace files are loaded:**

Send this as your first message to Jarvis (via WhatsApp or the dashboard):

```
Hey Jarvis, run /context list and tell me which workspace files are loaded.
```

Expected response: All 7 core files listed as loaded (SOUL.md, IDENTITY.md, USER.md, MEMORY.md, AGENTS.md, HEARTBEAT.md, TOOLS.md).

**Test the persona:**

```
Who are you and what is your role?
```

Expected: Jarvis identifies as Chief of AI Staff, describes capabilities, references your company.

---

## Post-Installation

### Enable Heartbeat (when ready)

After 24-48 hours of stable operation, enable proactive behavior:

Edit `~/.openclaw/openclaw.json`:

```json
{
  "agent": {
    "heartbeat": {
      "every": "30m"
    }
  }
}
```

Restart: `sudo systemctl restart openclaw`

### Add Google Workspace (optional)

Install the `gog` skill for Gmail, Calendar, and Drive:

```bash
clawhub install gog
```

> **CRITICAL:** Use a dedicated agent account (e.g., jarvis@yourcompany.com), never your personal Gmail. Google can ban accounts that show automated behavior. Start with read-only permissions.

### Model Upgrade Path

| Model | Use Case | VRAM | Speed on GB10 |
|-------|----------|------|----------------|
| qwen3.5:27b | Quick tasks, testing | ~40GB | Fast |
| qwen3.5:35b-a3b | Daily operations (recommended) | ~35GB active | ~43 tok/s |
| gpt-oss-120b | Complex reasoning, analysis | ~65GB | Slower |
| qwen3.5:122b-a10b | Coding, technical work | ~50GB active | Moderate |

---

## Dell Pro Max GB10 Optimization Notes

The Dell Pro Max GB10 (NVIDIA DGX Spark) is the ideal hardware for Jarvis:

- **128GB unified memory** — Run models up to 120B parameters entirely on-device
- **NVIDIA Grace Blackwell GPU** — Tensor Cores optimized for AI inference
- **Always-on Linux** — Designed for 24/7 operation, perfect for an always-on agent
- **1.9TB+ storage** — Room for multiple models, RAG indexes, and workspace history
- **Thermal design** — Sustained 70°C under heavy load is normal and healthy

**Performance tips:**

1. Use MoE models (like Qwen3.5-35B-A3B) — they activate fewer parameters per request, giving better speed-to-capability ratio
2. Set GPU to performance mode: `sudo nvpmodel -m 0 && sudo jetson_clocks`
3. Monitor thermals: GPU should stay below 85°C under sustained load
4. Keep at least 20GB RAM free for the OS and OpenClaw gateway
5. Use NVFP4 quantization for larger models (see NVIDIA playbook at build.nvidia.com/spark/nvfp4-quantization)

---

## Memory Architecture

Jarvis uses a 3-tier memory system designed for long-term reliability:

```
Tier 1 — Always Loaded (every session)
├── SOUL.md        → Who Jarvis is
├── IDENTITY.md    → Name and voice
├── USER.md        → Who you are
├── MEMORY.md      → Curated long-term facts (keep under 100 lines)
├── AGENTS.md      → Operating rules
├── HEARTBEAT.md   → Proactive checklist
└── TOOLS.md       → Environment config

Tier 2 — Auto-loaded (today + yesterday)
└── memory/YYYY-MM-DD.md  → Daily observations

Tier 3 — Searched on demand (semantic)
├── memory/people/     → Contact profiles
├── memory/projects/   → Project status
├── memory/topics/     → Domain knowledge
└── memory/decisions/  → Decision log with rationale
```

**Critical rule:** Put durable instructions in FILES, not in chat messages. Chat messages are lost during context compaction. Everything in Tier 1 files survives compaction.

---

## Security Model

Jarvis follows a defense-in-depth security approach:

1. **Isolation** — Run on a dedicated or clean DGX Spark, not your primary workstation
2. **Least privilege** — Dedicated agent accounts with minimum access
3. **Skill vetting** — Only install community-vetted skills; audit source code
4. **Network security** — Never expose the web UI to public internet; use Tailscale VPN
5. **Firewall** — UFW rules to restrict agent's outbound connections
6. **Monitoring** — Daily log review, heartbeat health checks
7. **Approval gates** — External messages, file modifications, and bulk operations require human confirmation
8. **Git-backed workspace** — All memory and config changes are version-controlled and recoverable

**This skill contains NO:**
- Network calls to external endpoints
- Obfuscated or encoded code
- Filesystem access outside the OpenClaw workspace
- Requests for API keys or credentials
- Background processes or daemons
- Binary downloads or package installations beyond declared dependencies

---

## Troubleshooting

**Jarvis doesn't know who he is:**
- Run `/context list` to check if SOUL.md and IDENTITY.md are loaded
- Verify files exist in `~/.openclaw/workspace/`
- Check file sizes are under 20,000 characters each
- Restart the gateway: `sudo systemctl restart openclaw`

**Memory is not persisting:**
- Check that MEMORY.md exists and is under 100 lines
- Verify daily memory files are being created in `memory/`
- Look for "dirty" memory warnings in the dashboard
- Ensure the workspace is writable: `ls -la ~/.openclaw/workspace/`

**GPU overheating (>85°C):**
- Check ambient temperature and airflow
- Reduce model size or context window
- Run `nvidia-smi` to check current utilization
- Consider enabling speculative decoding for efficiency

**WhatsApp not responding:**
- Check channel authentication in the dashboard
- Verify allowlist configuration includes your number
- Restart gateway and re-scan WhatsApp QR code

---

## Uninstall

To remove Jarvis persona files while keeping OpenClaw intact:

```bash
# Back up first
cp -r ~/.openclaw/workspace ~/.openclaw/workspace.jarvis-backup.$(date +%Y%m%d)

# Remove Jarvis-specific files
rm ~/.openclaw/workspace/SOUL.md
rm ~/.openclaw/workspace/IDENTITY.md
rm ~/.openclaw/workspace/HEARTBEAT.md

# Restart gateway
sudo systemctl restart openclaw
```

Your USER.md, MEMORY.md, and AGENTS.md can be kept or customized for a different persona.

---

## Credits & Resources

**Skill Author:** [Yogesh Huja](https://www.linkedin.com/in/yogeshhuja/) — Founder & CEO, Gignaati (Smartians AI Pvt. Ltd)

**Book:** [Invisible Enterprises: How to Lead Better with People & AI Agents](https://www.invisible-enterprises.com/) by Yogesh Huja — The best-selling guide for leaders navigating the intersection of human talent and AI-powered operations.

**Powered by:** [Gignaati](https://gignaati.com) — Making enterprise AI accessible, affordable, and local-first.

**References:**
- [NVIDIA DGX Spark OpenClaw Playbook](https://build.nvidia.com/spark/openclaw)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Qwen3.5 + OpenClaw on GB10 Guide](https://github.com/ZengboJamesWang/Qwen3.5-35B-A3B-openclaw-dgx-spark)
- [OpenClaw Gateway Security](https://docs.openclaw.ai/gateway/security)
- [ClawHub (Community Skills)](https://clawhub.ai)

**License:** MIT — Use freely, modify freely, attribute kindly.

**Version:** 1.0.0 | **Last Updated:** 2026-03-16
