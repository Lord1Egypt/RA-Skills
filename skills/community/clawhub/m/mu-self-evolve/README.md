<p align="center">
  <img alt="mu-self-evolve" src="assets/default-banner.png" width="100%">
</p>

# 🧬 mu-self-evolve · Agent自我反思与进化器

> A continuous self-evolution system for AI Agents — daily experience sedimentation + weekly error reflection, turning scattered conversations into structured persistent memory.

**English** | [中文](README_CN.md) | [🌐 Landing Page](https://muippt.github.io/mu-self-evolve/)

[![WeChat](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![Xiaohongshu](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![Book](https://img.shields.io/badge/Book-Visual%20Team%20Management-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skillhub](https://img.shields.io/badge/mu--skillhub-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-self-evolve)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-self-evolve)](https://github.com/muippt/mu-self-evolve/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-self-evolve)](https://github.com/muippt/mu-self-evolve/stargazers)

### 💡 Usage Examples

🧠 **Daily Experience Sedimentation** — Automatically extract corrections, errors, and positive signals from today's conversations and log them into structured files.

🔗 **Broken-Loop Protection (v3.1)** — Trigger signals are written to the daily diary the moment they occur; when the diary is missing, the cron proactively rebuilds it from real traces of the day. The evolution loop never runs dry.

🔍 **VFM Verification** — Before promoting any rule to permanent memory, run deterministic verification scripts that check recurrence count, cross-task scope, and resolution rate.

🪶 **Score-Based Eviction** — Memory entries decay over time with a 30-day half-life formula; low-value entries are archived automatically while high-recurrence ones are exempt.

🏷️ **WHERE×WHY Pathology Archiving** — Every error is tagged with WHERE (error stage) and WHY (root cause type), enabling structured pattern analysis instead of vague narratives.

🧪 **Bias Audit** — Inject synthetic test entries with known properties to verify the eviction mechanism catches them correctly — like a fire drill for your memory system.

🔗 **Broken-Loop Protection (new in v3.1)** — The most dangerous failure isn't an error, it's silent idling: the cron runs on time every day, but the diary (its sole data source) stays missing — so the system "punctually records that it did nothing". v3.1 fixes both ends: ① in-session trigger signals (corrections / errors / feature requests / positive feedback / key decisions) are written to the daily diary immediately — batching at session end is forbidden; ② when the cron finds the diary missing, instead of skipping, it rebuilds the diary from three kinds of real traces of the day (cron run logs, same-day long-term-memory entries, workspace file changes) before running the 6 steps. Fabrication strictly forbidden.

🛠️ **Active Skill Synthesis** — When ≥3 entries in the same domain cluster together, automatically generate a Skill draft (SKILL.md skeleton + script framework) for the human to review.

⏰ **Scheduled Automation** — Set up daily cron jobs that run the full 6-step evolution workflow, with an extended weekly reflection every Friday.

📊 **Cross-Environment Support** — Auto-detects OpenClaw, Claude Code, or other LLM agent environments, adapting paths and scheduling automatically.

---

### ✨ Core Highlights

#### 🔍 Don't Trust, Verify — The AI Can't Promote Itself

AI agents are great at spotting patterns, but terrible at judging whether those patterns are worth remembering permanently. An agent might say "I've learned this rule is important!" — but how do you know it's not hallucinating confidence?

mu-self-evolve separates **proposing** from **verifying**. The agent proposes a rule, then a Python script checks actual data: how many times has this error recurred? Across how many different tasks? Has the proposed solution actually been confirmed to work? Only when the data backs it up does the rule get promoted to permanent memory.

Think of it like a student who claims they've mastered a topic — you don't just take their word for it, you give them a test with real questions.

| Step | Who | What |
|------|-----|------|
| Propose | Agent | "I noticed this pattern keeps happening" |
| Verify | Script | Counts recurrence, cross-task scope, resolution rate → confidence score 0–100 |
| Promote | Gate | Confidence ≥70 + Recurrence ≥2 → write to permanent memory |

#### 🪶 Memories Fade Naturally — Like a Human Brain

Most memory systems either keep everything forever (until you manually delete) or truncate by line count (delete the oldest entries when the file gets too long). Both are bad: forever-keeping means noise drowns signal; line-count truncation might delete a crucial rule just because it's old.

mu-self-evolve uses a **time-decay formula** — each memory's importance score naturally decreases over time, just like how you forget the details of a book you read months ago, but vividly remember lessons that keep coming up in conversations.

Memories that get referenced regularly get their freshness reset. Memories that nobody touches for 30 days lose half their score. But memories that have proven useful across multiple tasks are permanently exempt — they've earned their place.

```
effective_score = VFM × 0.5^(days_since_last_seen / 30)
```

#### 🏷️ Every Mistake Gets a Diagnosis, Not Just a Description

When something goes wrong, most systems log "Error: something failed." That's about as useful as a doctor writing "Patient is sick" — you know something happened, but you can't spot patterns.

mu-self-evolve tags every error with two labels: **WHERE** (which stage did it happen at?) and **WHY** (what was the root cause?). This turns a pile of vague error logs into a structured matrix where you can instantly see patterns like "huh, 80% of our errors are in the MCP call stage, and the root cause is always token expiration."

**WHERE** (where did it break): `skill_load` · `mcp_call` · `file_write` · `api_call` · `browser_op` · `memory_op` · `agent_dispatch` · `prompt_parse` · `auth` · `other`

**WHY** (why did it break): `param_missing` · `token_expired` · `timing_race` · `perm_denied` · `knowledge_gap` · `format_mismatch` · `timeout` · `logic_error` · `config_drift` · `user_correction` · `other`

Both sets are customizable — add your own tags as your agent encounters new environments.

#### 🧪 The Garbage Collector Tests Itself

Here's a scary thought: what if the memory-cleaning mechanism itself is broken, silently deleting valuable memories while everything looks fine on the surface? You'd never know — the system reports "archived 5 entries" and you trust it, not realizing 3 of those should have been kept.

mu-self-evolve defends against this using **defect injection testing** — **injecting fake test entries with known properties** into the system — entries that are designed to be kept, archived, or exempted. After running the eviction logic, it checks whether each fake entry was handled correctly. Any mismatch means the eviction logic has a bug.

Think of it like a quality inspector who tests the quality inspector — if the checking mechanism itself is broken, everything looks fine when it's not.

---

### 📌 Comparison

| Feature | mu-self-evolve | Raw Memory Files | Cloud Memory API | Vector Database |
|---------|---------------|-------------------|------------------|------------------|
| Daily auto-sedimentation | ✅ 6-step workflow | ❌ Manual | ❌ API-only | ❌ Requires integration |
| Broken-loop protection | ✅ Instant write + backfill rebuild (v3.1) | ❌ | ❌ | ❌ |
| Deterministic verification | ✅ Script-based | ❌ | ✌️ LLM self-assessment | ❌ |
| Time-decay eviction | ✅ 30-day half-life | ❌ | ✌️ Yes | ✌️ Yes |
| Pathology archiving (WHERE×WHY) | ✅ Structured tags | ❌ | ❌ | ❌ |
| Bias audit | ✅ Defect injection | ❌ | ❌ | ❌ |
| Active Skill synthesis | ✅ Cluster → draft | ❌ | ❌ | ❌ |
| Cross-environment support | ✅ OpenClaw + Claude Code | N/A | ❌ | ❌ |
| No external API required | ✅ Fully local | ✅ | ❌ | ❌ |

---

### 🚀 Workflows

| Workflow | Scenario | Trigger |
|----------|----------|---------|
| Daily Evolution (Steps 1-6) | Extract today's experiences, verify, promote, summarize | Scheduled cron (daily) |
| Diary backfill (v3.1) | Rebuild the diary from real traces when missing, preventing an empty loop | Cron pre-step |
| Weekly Reflection (Steps 6a-6g) | Error scanning, narrative generation, eviction, Skill synthesis | Friday (merged with daily) |
| On-Demand Recording | User corrects agent or error occurs | Trigger detection (real-time, written to diary immediately) |
| Manual Verification | Check a specific rule's confidence | `python3 vfm_verify.py <pattern-key>` |
| Eviction Audit | Run bias test + score-based cleanup | `python3 bias_audit.py && python3 eviction_score.py` |

---

### ⚙️ Technical Specs

| Item | Description |
|------|-------------|
| Runtime | Python 3.8+ (scripts only); any LLM Agent (OpenClaw / Claude Code / Cursor) |
| Dependencies | Zero external packages — standard library only |
| Storage | Local markdown files (no database, no API) |
| Scripts | 4 Python files: `env_detect.py`, `vfm_verify.py`, `eviction_score.py`, `bias_audit.py` |
| References | 4 docs: `record-templates.md`, `weekly-reflection.md`, `file-structure.md`, `claude-code-compat.md` |
| Total Size | ~45KB (excluding banner) |
| Scheduling | `openclaw cron` or system `crontab` |

---

### 🛠️ Quick Start

```bash
# 1. Clone
git clone https://github.com/muippt/mu-self-evolve.git

# 2. Initialize (auto-detects environment)
cd mu-self-evolve
python3 scripts/env_detect.py --init

# 3. Schedule daily evolution
openclaw cron add --name "🧬 Daily Evolution" --cron "30 19 * * *" --message "Run mu-self-evolve daily workflow"
```

That's it. The agent will start sedimenting experiences daily and reflecting weekly.

---

### 🔒 Security & Privacy

- **100% Local** — All data stays in your workspace's `.learnings/` directory. No cloud, no API calls, no telemetry.
- **No External Dependencies** — Python scripts use only the standard library.
- **No Model Parameters** — Works by organizing text in markdown files, not by fine-tuning or updating weights.
- **User-Controlled Eviction** — Every archive decision is logged; the bias audit ensures transparency.

---

### ⭐ Star History

If mu-self-evolve helps your agent get smarter, consider giving it a star ⭐

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-self-evolve&type=date)

> An AI Agent that learns from its own mistakes — no fine-tuning required.

---

### 👤 About the Author

🎓 Signatory Author of Tsinghua University Press / 2026 Dangdang Influential Author / AI & Large Model Business HR Specialist at a Leading Tech Company / National Level-1 HR Manager / Level-2 Psychological Counselor / Self-taught Designer

📚 Author of [*Visual Team Management*](https://item.m.jd.com/product/14547345.html). Clients include ByteDance, Tencent, Baidu, China Mobile, SMG, BOE…

💡 [WeChat Official Account](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [Xiaohongshu](https://xhslink.com/m/ESxtgUNMdl): muippt

---

### 📄 License & Acknowledgments

[MIT](LICENSE) © 2026 muippt

> Note: Much of this project was co-created with AI assistance. If you believe your work has been used without proper attribution, please open an issue.
