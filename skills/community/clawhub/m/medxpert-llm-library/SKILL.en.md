---
name: medxpert-llm-library
description: "🌐 Website: https://medxpert.cn (MedXpert medical-device registry knowledge base, public free tier). One-liner: your old laptop can run local LLMs and build a knowledge base — no GPU purchase needed. Full chain: old-PC hardware check (0 cost) → Ollama local deploy (Qwen2.5/DSH UI) → knowledge base in 3 tiers → RAG retrieval Q&A (bge-m3) → library management (classification/version/retrieval/QC/permissions/confidentiality) → content monetization (membership/WeChat account/skill traffic) → knowledge base online (website/IMA/Huawei/Xiaoyi). Triggers: how to set up a knowledge base / how to run LLMs / can my computer run LLMs / can a low-spec PC run LLMs / how to use an old computer / how to connect DSH to Ollama / how to divide multi-model work / how to do RAG / how to monetize a knowledge base / local deployment / save API credits / offline use / privacy AI. Note: this skill focuses on local LLMs and knowledge bases, not cloud API deployment or software development."
agent_created: true
version: "1.29.1"
---

# Local LLMs + Personal Library: A Low-Spec Computer Practical Guide

> **🌐 Website: https://medxpert.cn** (MedXpert medical-device registry knowledge base, public free tier, AI-readable llms.txt) — a live example of this skill's methodology.
> **One-liner: your old laptop can run LLMs. No GPU purchase. No 10k workstation.**

> **⏱️ TL;DR (30 seconds)**: ① An old 8GB-RAM PC runs local LLMs (qwen2.5:3b) — no high-spec hardware needed; ② Install Ollama + one command to pull a model; use quickstart.py to build a personal knowledge base (summary/retrieval/Q&A); ③ Add DSH UI and RAG for a better experience, see Business Logic for monetization.

## Panorama: One Picture, Whole Skill (10-second overview)

> This skill is one complete chain: **old PC → local model → knowledge base → Q&A → library → monetization → AI ecosystem**. Each link maps to sections — use what you need, no need to read top to bottom.

```
Old PC(0 cost) → Local Model(Ollama) → Knowledge Base(3 tiers) → RAG(Q&A) → Library(5 tools) → Monetization(membership) → AI Ecosystem(website/Agent)
   [0, 1]            [2, 3]                [4]                   [4+]         [5]              [5+ series]              [5+10]
```

**One-liner per link**:

| Link | One-liner | Section |
|------|-----------|---------|
| ① Old PC works | 8GB RAM, no GPU — 0 cost to start | 0, 1 |
| ② Local model | Ollama one-command deploy, Qwen2.5 great for Chinese | 2, 3 |
| ③ Knowledge base | Files / RAG tools / custom pipeline — pick your tier | 4 |
| ④ RAG Q&A | bge-m3 cross-lingual retrieval + chunk tuning, answers with sources | 4+ |
| ⑤ Library mgmt | Classification/version/retrieval/QC/security — value compounds | 5 |
| ⑥ Monetization | Membership/WeChat account/skill traffic — low cost, high income | Business, 5+ |
| ⑦ AI ecosystem | Connect knowledge base to website/IMA/Huawei/Xiaoyi for AI use | 5+10 |

> **One-line summary: spend the least (hardware $0, credits $0), use the most models (Qwen/DeepSeek/VL/Embedding teamwork), build a private library that is safe (offline), transparent (trackable), and controllable (tiered permissions).**

## Environment Requirements & Reliability

**One command self-check**: `python quickstart.py doctor` — checks 5 items (Python / requests / Ollama / disk space / library dir), each failure comes with a fix command. Re-run to re-verify.

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8+ | 3.10+ |
| Ollama | 0.1.x+ | Latest |
| RAM | 8GB (3B model) | 16GB (7B model) |
| Disk | 5GB free | 10GB+ |

**Reliability guarantees**: auto-retry with exponential backoff (network jitter / Ollama hang, 3 tries) · human-readable errors with fixes (no stack traces) · input tolerance (empty / non-UTF-8 / unreadable files are skipped, never crash) · idempotent `init` (re-runnable, no side effects) · honest answers (explicitly says "not found in knowledge base" instead of fabricating) · China-network friendly (mirror sources + retry + doctor check).

---

## Core Selling Points: Six Capabilities (30-second read)

| # | Capability | One-liner |
|---|-----------|-----------|
| 1 | **Low-cost feeding** | Local models burn zero API credits; batch feeding costs near zero |
| 2 | **Multi-model nightly learning** | Feed different files to different models; they learn overnight, results by morning |
| 3 | **Effective library management** | Classification/versioning/retrieval/QC/operations — knowledge compounds |
| 4 | **Data security, offline** | Fully local, works without internet, data never leaves your machine |
| 5 | **File tracking** | Git full history + audit logs — who changed what, when, is always clear |
| 6 | **Permission management** | Tiered roles + access control + encryption + watermarking |

---

## Business Logic: Low Cost → High Income

| Cost item | How much | How to save |
|-----------|----------|-------------|
| Hardware | **$0** | Use your existing/old computer |
| Compute | **$0** | Local models are free, no API credits |
| Time | **$0 (daytime)** | Nightly batch tasks, models work while you sleep |
| Tools | **$0** | Free toolchain (Ollama/AnythingLLM/Git) |
| Acquisition | **$0** | Content + skill self-traffic, no ads |

**Income streams**: Membership card ($15-30/yr) → paid topic packs ($7/pack) → 1-on-1 consulting ($70+/session) → **B2B library customization ($5k+/client — one deal = a year of memberships)**.

**Four levers**: Content (1 source → 12+ posts) / Tool (publish a skill = unlimited brand exposure) / Time (nightly tasks = 24h working) / Compounding (content + open source grow value).

---

## 0. Low Hardware: Not a Compromise, a Smart Choice

- **CPU-only** (no GPU) runs 3B-7B models at usable speed
- **8GB office laptop** runs Qwen2.5:3B, good Chinese, fast responses
- **16GB** runs 7B — daily Q&A, document summarization, knowledge retrieval all work
- A knowledge base does **not** require a RAG framework — files + scripts work fine

**Old computer as server**: close-lid running, phone/tablet browser access, Tailscale for anywhere access (free).

**Optimization three tricks**: Q4 quantization (1/3-1/4 size) / control context (8192-16384) / serial processing (one batch task at a time).

---

## 1. Hardware Check: What Can Your Computer Run?

| Memory | Recommended model | Notes |
|--------|------------------|-------|
| 4GB | qwen2.5:0.5b | Usable but limited |
| **8GB** | **qwen2.5:3b** | **Best value** |
| **16GB** | **qwen2.5:7b** | **Recommended, near online quality** |
| 32GB | qwen2.5:14b | Stronger reasoning |
| 48GB+ | qwen2.5:32b | Near GPT-3.5 level |

Check commands: `wmic computersystem get TotalPhysicalMemory` (Windows) / `system_profiler SPDisplaysDataType` (macOS).

---

## 2. Deployment: Ollama (Recommended)

```bash
# Windows: download https://ollama.com/download (or gh-proxy mirror)
# Always verify SHA256 after proxy download
curl -L -o OllamaSetup.exe "https://gh-proxy.com/https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe"
curl -L -o sha256sum.txt "https://gh-proxy.com/https://github.com/ollama/ollama/releases/latest/download/sha256sum.txt"
sha256sum OllamaSetup.exe   # compare with sha256sum.txt
./OllamaSetup.exe /S

ollama pull qwen2.5:3b
ollama run qwen2.5:3b
curl http://localhost:11434/api/tags   # verify
```

**China network tip**: wrap pulls with retry: `for i in $(seq 1 15); do timeout 480 ollama pull <model> && break; done`

**DSH (DeepSeek Harness) frontend**: `npm install -g @anthropic/dsh` (use npmmirror registry in China), gives ChatGPT-style UI with Agent mode.

---

## 3. Multi-Model Collaboration: Different Models, Different Jobs

| File type | Feed to | Why |
|-----------|---------|-----|
| PDF scans/images | **Qwen2.5VL:3B** (vision) | Only model that "sees" images |
| Chinese text/web | **Qwen2.5:7B** | Best Chinese summarization |
| Tables/data | Qwen2.5:14B | Better numbers/columns |
| English docs | Qwen2.5:7B or Llama 3.2 | English native |
| Code/tech docs | **DeepSeek-R1:7B** | Strongest code/reasoning |
| Complex analysis | DeepSeek-R1:7B/8B | Deep reasoning |
| Long docs | Chunk first → Qwen 7B batch → merge | Prevents truncation |

> **One-liner**: Vision for images, Qwen for Chinese, DeepSeek for thinking, chunk long docs.

---

## 4. Knowledge Base Setup (Three Tiers)

| Tier | Approach | Tools | Time |
|------|----------|-------|------|
| Beginner | Files + scripts | quickstart.py | 10 min |
| **Advanced** | RAG tools | AnythingLLM/Cherry Studio | 30 min |
| Expert | Custom pipeline | LangChain + Chroma + Ollama | 1-3 days |

**Recommended library structure**:
```
my-library/
  00-index.md
  01-法规/ (regulations)
  02-产品/ (products)
  03-标准/ (standards)
  04-学习笔记/ (notes)
  changelog.md
```

---

## 5. RAG in Practice (Retrieval-Augmented Q&A)

**Workflow**: documents → chunk (500-800 chars) → embed → vector store → retrieve Top-K → prompt → answer with sources.

**Best practices**:
- **Embedding: bge-m3** — supports 100+ languages, cross-lingual retrieval (ask in Chinese, retrieve English FDA docs)
- Chunk size 500-800, overlap 50
- Top-K 5-8
- Hybrid search (vector + BM25) for technical terms
- Prompt: "only answer from sources, cite file names, say 'not found' if missing"

**Verification (10 questions)**: recall (in-library questions answered) / faithfulness (answers traceable to sources) / rejection (out-of-library questions clearly rejected) / citation (sources cited).

---

## 6. Library Management Essentials

| Area | Key points |
|------|-----------|
| Classification | 3-layer: domain → category → document; MECE principle |
| Ingestion | Desensitize first, add frontmatter (title/source/status/level/tags) |
| Versioning | Git + changelog.md + last_updated stamps |
| QC | Monthly model check: mark outdated, update, archive |
| Operations | Daily ingest / weekly index / monthly QC / quarterly review |
| Nightly tasks | `schtasks` (Win) or cron: batch summarize at 23:00 |
| File tracking | Git full history + audit logs + access logs |
| Permissions | Roles (admin/editor/read-only), dir-level tiers, Ollama localhost-only, Web UI passwords |
| Security | Desensitization, local isolation, AES-256 encryption, watermarks, no remote-control software |
| AI-friendly | llms.txt + robots.txt + README-ai.md + Markdown-first + semantic naming |

---

## 7. Monetization: From Library to Income

**Tiered content**: L0 free (traffic) / L1 followers (conversion) / L2 members (revenue) / L3 custom (high-value).

**WeChat Official Account**: 70% value + 20% cases + 10% monetization; 2-3 posts/week; traffic main from killer titles + hooks + QR code.

**Multi-platform matrix**: XHS cards / Zhihu answers / Bilibili videos / Douyin shorts / X & LinkedIn English posts. One source → 12+ pieces.

**Library-as-IP**: "follow = library card, pay = upgrade borrowing rights". Free reader card / membership card ($15-30/yr) / curator consulting ($70+/session) / B2B library building ($5k+).

**Skill-driven traffic**: publish your methodology as a skill — every use is brand exposure. Author credit, README hooks, version updates.

**AI payment (get ready early)**: WeChat AI Card (consumer side, in-chat payments) + SkillPay/Pay Skills (creator side, charge per call). **Tokenization**: in-platform knowledge coins (compliant) → e-CNY (official, zero fee) → NFT/digital collectibles (regulated, licensed platforms only).

**International**: language-split dirs (zh/en), bge-m3 cross-lingual RAG, FDA/MDR/ISO English docs, X/LinkedIn English content.

---

## 8. Quick Start (10 minutes to first answer)

```
□ 1. Check memory: 8GB+? continue. 4GB? use qwen2.5:0.5b
□ 2. Install Ollama: https://ollama.com/download
□ 3. ollama pull qwen2.5:3b
□ 4. ollama run qwen2.5:3b  (test chat)
□ 5. python quickstart.py init  (create library structure)
□ 6. Put your .md/.txt docs into folders
□ 7. python quickstart.py summarize  (batch summarize)
□ 8. python quickstart.py ask "your question"  (ask)
□ 9. python quickstart.py health  (health check)
```

---

## 9. FAQ (Top questions)

**Q: Slow responses?** A: Use a smaller model (7B→3B); close memory hogs; verify GPU usage (`ollama ps`).
**Q: Poor Chinese?** A: Use Qwen2.5 series; bigger model (3B→7B); prompt "answer in Chinese".
**Q: Can't pull models in China?** A: gh-proxy for installer; retry loop for pulls; start with small models.
**Q: RAG answering wrong?** A: Check embedding (use bge-m3 for Chinese), chunk size (500-800), hybrid search.
**Q: RAG making things up?** A: Prompt "only from sources + cite + say not found"; lower Top-K; raise threshold.
**Q: Need internet?** A: No, fully offline after setup. Only download/install needs network.

---

## 10. Troubleshooting Quick Table

| Symptom | Fix |
|---------|-----|
| Ollama unreachable | `ollama serve`; verify `curl localhost:11434/api/tags` |
| Model pull fails | retry loop with timeout; smaller model |
| Slow answers | smaller model; free memory; GPU check |
| Bad Chinese | Qwen2.5; prompt in Chinese |
| DSH EMPTY_RESPONSE | pi-ai patch (see DSH section) |
| RAG wrong/making up | bge-m3; chunk 500-800; Top-K 5-8; strict prompt |
| OOM | serial processing; `OLLAMA_KEEP_ALIVE` short; Q4 quant |
| Remote access fails | Tailscale (easiest) |

---

## Templates (templates/ directory)

- `llms.txt` — AI library map (root of your library)
- `README-ai.md` — AI usage instructions (root of your library)
- `frontmatter-template.md` — metadata template for ingested files
- `copyright-disclaimer-template.md` — copyright + disclaimer for published works
- `library-account-copy.md` — library-account copywriting kit (cards/opening-day/membership/coins)

---

## License & Disclaimer

**Copyright © 2026 注册老炮 (ZhuCeLaoPao) · MIT License**

1. **Reference only**: content is based on personal experience for learning exchange, not professional/legal/medical advice.
2. **AI-generated content**: may contain errors; always verify against official/current versions.
3. **Medical device note**: content on regulations is for practitioner reference only, not compliance advice; consult qualified institutions and follow current regulations.
4. **Use at your own risk**: follow instructions at your own risk; back up data; author not liable for losses.
5. **Third-party liability**: third-party tools/links belong to their owners.
6. **Timeliness**: content reflects publish-time information; verify latest versions.
