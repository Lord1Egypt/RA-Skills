# Hive-Commander: Distributed Intelligence Kernel 🐝

> **"One brain is a tool; a hive is a weapon."**
> 
> A production-grade "1+5" asynchronous agentic harness for OpenClaw. Inspired by Kimi's Agentic Workflow and Mitchell Hashimoto's Harness Engineering.

---

### 🌪️ The "Recruitment" Engine
Hive-Commander transforms your skill library into a dynamic workforce:
- **Auto-Discovery**: Scans your local skills via `meta-router`.
- **Dynamic Mounting**: Injects third-party skill logic directly into parallel worker agents.
- **Resilient Execution**: Built-in exponential backoff for API rate-limits and sequential fallback modes to ensure delivery.

### 🔗 Integrated Ecosystem
Installs and manages the core cognitive arsenal automatically:
- `meta-router`: For skill indexing (Required for Recruitment).
- `48h-expert`: For vertical scanning nodes.
- `first-principles`: For logical auditing nodes.

---
### 🛡️ Security & Transparency

**Hive-Commander** is a high-privilege meta-orchestrator. To ensure user safety, it adheres to the following security protocols:

- **Local-Only Execution**: The `executor.py` script only interacts with the official OpenAI/Anthropic API and local `swarm_tmp` directory. No telemetry or hidden exfiltration.
- **Path-Restricted**: Access is strictly limited to the `~/.openclaw/` workspace. It does not touch `~/.ssh`, `~/.aws`, or browser profiles.
- **Audit-Ready**: All worker outputs are saved as transparent `.md` files in `~/.openclaw/swarm_tmp/` for human review.
- **Sandboxing Recommended**: For maximum security, we recommend running OpenClaw in a **Docker** container or a dedicated VM when using multi-agent swarms.

### 🚀 Usage
Simply start your query with `hive:` or `swarm:`.
Example: `hive: Analyze the 2026 solid-state battery market from tech and cost perspectives.`

### 💻 Installation
```bash
clawhub install hive-commander

Author: Lawliet | License: MIT