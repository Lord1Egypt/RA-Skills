# 🔬 MiroMind Deep Research Skill

> A deep research skill for [OpenClaw](https://openclaw.ai) that automates DeepResearch tasks by controlling the MiroMind website via playwright-mcp.
> 
> MiroMind uses their latest MiroThinker-1.7 (235B parameter model) to perform long-chain reasoning and multi-round verification on any topic, and automatically saves a complete Markdown report.

[![Platform](https://img.shields.io/badge/platform-OpenClaw-blue)](https://openclaw.ai)
[![Model](https://img.shields.io/badge/model-MiroThinker--1.7%20235B-purple)](https://dr.miromind.ai)
[![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-green)](#)

---

## Highlights

- **One-line trigger**: Just type `/miromind your question` to start a deep research session
- **MiroThinker-1.7 (235B)**: Large-scale reasoning model with long chain-of-thought and multi-round self-verification
- **URL-based submission**: Directly submits research via URL parameters — no button clicks, highly reliable
- **Async polling + real-time feedback**: Returns a live Chat URL so you can watch progress in your browser
- **Auto-save reports**: Generates a complete Markdown report saved to your local workspace
- **Cross-platform**: Works on Windows, macOS, and Linux

---

## Prerequisites

| Dependency | Description |
|------------|-------------|
| [OpenClaw](https://openclaw.ai) | Runtime environment |
| `playwright-mcp` Skill | Browser automation for controlling the MiroMind website |
| [MiroMind Account](https://dr.miromind.ai) | Required to log in and use MiroThinker AI |

---

## Installation

```bash
# 1. Install this skill
clawhub install miromind

# 2. Install the Playwright MCP Skill (browser automation dependency)
clawhub install playwright-mcp

# 3. Install the Playwright browser engine
npx playwright install chromium
```

---

## Configuration

### Step 1: Create a MiroMind account

Sign up at [https://dr.miromind.ai](https://dr.miromind.ai).

### Step 2: Add credentials to OpenClaw

Open the OpenClaw config file:

```bash
openclaw config edit
```

Add the following under the `env` section:

```json
{
  "env": {
    "MIROMIND_EMAIL": "your@email.com",
    "MIROMIND_PASSWORD": "your-password"
  }
}
```

### Step 3: Restart the Gateway

```bash
openclaw gateway restart
```

> ⚠️ If credentials are missing, the skill will display a friendly setup guide instead of failing silently.

---

## Usage

```
/miromind [topic or question]
```

### Examples

```bash
# Financial analysis
/miromind Predict the gold price trend for 2026

# Technology research
/miromind Latest breakthroughs in quantum computing

# Company analysis
/miromind Analyze NVIDIA's latest earnings report

# Fact-checking
/miromind Investigate the truth behind [news event]

# Trend forecasting
/miromind AI industry development trends in 2026
```

---

## Execution Flow

```
User types /miromind [question]
        ↓
Check MIROMIND_EMAIL / MIROMIND_PASSWORD env vars
        ↓
Spawn sub-agent (isolated session, 15-min timeout)
        ↓
Sub-agent executes:
  1. Navigate to https://dr.miromind.ai/
  2. Check login status — auto-login if needed
  3. Submit research via URL parameter:
     → https://dr.miromind.ai/?noReleaseNotes&query=<encoded question>
  4. Capture the research Chat URL and return it to user immediately
  5. Poll every 10 seconds for completion (max 20 minutes)
  6. Research done → extract full content from the page
  7. Save complete Markdown report to local workspace
        ↓
Returns: research summary + local report path + Chat URL
```

---

## Output

Reports are automatically saved to:

```
~/.openclaw/workspace/skills/mirothinker/outputs/
└── mirothinker-<timestamp>.md
```

Report format:

```markdown
# MiroMind Deep Research Report

**Topic**: Your question
**Date**: 2026-03-20 12:34:56

---

(Full MiroThinker research content)
```

---

## Technical Details

| Feature | Description |
|---------|-------------|
| URL submission | Uses `?noReleaseNotes&query=` to create a research session directly, bypassing unreliable button clicks |
| Async sub-agent | Runs via `sessions_spawn` in an isolated session, non-blocking for the main conversation |
| Polling strategy | Checks page status every 10 seconds, up to 20 minutes maximum |
| Content extraction | Uses `page.evaluate()` to read `innerText`, compatible with dynamically rendered content |
| Cross-platform | Tested on Windows, macOS, and Linux |

---

## FAQ

**Q: How long does a research session take?**  
A: Typically 3–10 minutes, longer for complex topics. The skill returns a Chat URL immediately so you can track progress in real time.

**Q: What if the page doesn't redirect to `/chat/` after submission?**  
A: This usually indicates a network issue or expired login session. The skill will report an error with details — simply re-run the command.

**Q: Where are the reports saved?**  
A: In `~/.openclaw/workspace/skills/mirothinker/outputs/`. The full path is printed at the end of each run.

**Q: Does it support questions in English?**  
A: Yes, MiroThinker supports both English and Chinese.

---

## Links

- **MiroMind**: [https://dr.miromind.ai](https://dr.miromind.ai)
- **OpenClaw**: [https://openclaw.ai](https://openclaw.ai)
- **ClawHub Skill Marketplace**: [https://clawhub.ai](https://clawhub.ai)

---

## License

MIT
