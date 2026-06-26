# 📰 ClawForage Knowledge Harvester

### Wake up to an AI that already read today's news.

Your agent fetches trending content overnight in your domains of interest, summarizes it, and stores it in memory — so next time you ask a question, it already knows the answer.

---

## ✨ What It Does

| Feature | How it helps |
|---------|-------------|
| **Automated fetching** | Pulls trending articles from Google News RSS — no API keys needed |
| **Smart summaries** | Condenses each article into 100-200 words of key facts and implications |
| **RAG-ready storage** | Drops Markdown into `memory/knowledge/` for automatic vector indexing |
| **Deduplication** | Never re-processes articles you've already seen |
| **Source attribution** | Every summary links back to the original source |

## 🚀 Install

```bash
openclaw skill install clawforage/knowledge-harvester
```

## ⚙️ Setup

**1. Configure your domains:**
```bash
mkdir -p memory/clawforage
cat > memory/clawforage/domains.md << 'EOF'
# My Domains
- AI agent frameworks
- startup news Asia
- renewable energy
EOF
```

**2. Run it:**

Runs automatically every day at **2am**, or invoke anytime:
```
/clawforage-knowledge-harvester
```

## 🛡️ Legal Safety

- ✅ Uses Google News RSS (public, free, no scraping)
- ✅ Stores summaries only — never reproduces source content
- ✅ Always attributes source with URL
- ✅ You control which domains to track

## 📋 Requirements

- `jq` — `brew install jq` or `apt install jq`
- `curl` — usually pre-installed
- `bash` (v4+)
- **No API keys required**

---

**Part of [ClawForage](../../README.md)** — built by [InspireHub Labs](https://inspireehub.ai)
| [Prompt Optimizer](../prompt-optimizer/) | [Research Agent](../research-agent/) |
