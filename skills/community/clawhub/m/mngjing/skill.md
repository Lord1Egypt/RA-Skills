# Mingjing — AI Agent Health Center

> Paste this into ClawHub publish page. Replace screenshot URLs with actual images.

---

## One-liner

Zero-dependency, offline-first LLM Agent health monitoring. pip install, zero LLM calls, ~40MB RSS.

## Screenshots

<!-- Replace with your screenshot URLs -->
- Health dashboard: `[screenshot-url]`
- Diagnosis report: `[screenshot-url]`

## Install

**Step 1** — Install backend:

```bash
pip install mingjing
```

**Step 2** — Enable probe in OpenClaw:

```bash
openclaw plugins install mingjing-probe
openclaw config set plugins.entries.mingjing-probe.enabled true
openclaw gateway
```

**Step 3** — Start web panel:

```bash
python3 -m src.ming start --daemon
python3 -m src.ming web start --port 18088
```

Visit `http://localhost:18088` to see live data.

## Features

| Feature | Description |
|---------|-------------|
| Zero dependencies | Pure Python stdlib, no third-party packages |
| Offline-first | No outbound traffic, data stored locally |
| Zero LLM cost | 157 rules, pure rule engine, no model calls |
| 7 framework adapters | LangChain / LlamaIndex / CrewAI / OpenHands / Semantic Kernel / AgentScope / Hermes |
| 4-level health grading | Healthy / Sub-healthy / Attention / Critical, per instance |
| Web dashboard | Live event stream, triage coverage, i18n (EN/中文), dark theme |

## Diagnostic capabilities (157 rules)

| Layer | Count | Covers |
|-------|-------|--------|
| System | 20+ | Memory, IO, CPU, disk, file descriptors |
| Probe | 8+ | Self-check, emit rate, buffer health |
| Agent | 20+ | Orchestration, steps, decisions, roles |
| Model | 15+ | Tokens, latency, output, frequency |
| Tool | 15+ | Duration, errors, output, execution |
| Network | 6+ | Connection, DNS, status codes |
| Security | 5+ | Injection, sensitive data leaks |
| Memory | 5+ | Retrieval, storage, windowing |
| Plugin | 10+ | Lifecycle, loading, errors |

## More

- Full docs: [Mingjing on GitHub](https://github.com/wulun811/Ming_qiankun)
- PyPI: `pip install mingjing`
- Report issues: https://github.com/wulun811/Ming_qiankun/issues