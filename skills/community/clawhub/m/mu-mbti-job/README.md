<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/default-banner.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/default-banner.png">
    <img alt="mu-mbti-job" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 🧬 mu-mbti-job · MBTI人格与职业测评

> Bilingual MBTI personality & career assessment with three depth levels (70/93/144 questions), producing professional PDF reports — runs 100% locally with zero dependencies.

**English** | [中文](README_CN.md) | [🌐 Landing Page](https://muippt.github.io/mu-mbti-job/)

[![WeChat](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![Xiaohongshu](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![Book](https://img.shields.io/badge/Book-Visual%20Team%20Management-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skillhub](https://img.shields.io/badge/mu--skillhub-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-mbti-job)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-mbti-job)](https://github.com/muippt/mu-mbti-job/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-mbti-job)](https://github.com/muippt/mu-mbti-job/stargazers)

### 💡 Usage Examples

- 🧬 **Personal self-assessment** — Pick a depth (quick 70 / standard 93 / pro 144 questions), finish in 10–25 minutes
- 📄 **Bilingual PDF report** — Four-dimension analysis, personality profile, career recommendations, interpersonal matches — all in Chinese & English side by side
- 👥 **Team composition analysis** — Aggregate results from multiple members into a team report with distribution heatmap and complementary pairing
- 💼 **Career direction reference** — Four suggested positions per type, each with reasoning and growth advice
- 🤝 **Interpersonal matching** — Best-partner and challenging types with concrete collaboration strategies
- 🔄 **Resume anytime** — Quiz page auto-saves progress and supports EN/中文 switching mid-test
- 🏠 **Team aggregation without a server** — Paste results into a conversation, or drop JSON files into a folder and run one command

---

### ✨ Core Highlights

#### 📊 Three Depth Levels in One Question Bank

| Level | Questions | Time | E/I · S/N · T/F · J/P |
|-------|-----------|------|------------------------|
| Quick | 70 | ~10 min | 16 · 19 · 18 · 17 |
| Standard | 93 | ~15 min | 21 · 26 · 24 · 22 (Form M structure) |
| Pro | 144 | ~25 min | 32 · 40 · 38 · 34 |

One bilingual 144-question superset (`data/questions.json`) — each version is a strict subset selected by `version_added` markers. The scoring engine validates dimension counts on startup and fails loudly on any mismatch.

#### 📑 Two Report Modes

| Report | Pages | Contents |
|--------|-------|----------|
| Personal | 5 | Cover, four-dimension analysis, personality profile (traits/strengths/blind spots/work style/decision/stress/communication), career recommendations, interpersonal matches |
| Team | 6 | Cover, member overview, 16-type distribution with trait snapshots, dimension heatmap, team strengths & blind spots, collaboration advice & complementary pairs |

#### 📄 Report Preview

| Cover | Four-Dimension Analysis | Career Recommendations |
|-------|-------------------------|------------------------|
| ![Cover](assets/report-page1.png) | ![Dimensions](assets/report-page2.png) | ![Careers](assets/report-page4.png) |

---

### 📌 Comparison

| Dimension | 🧭 mu-mbti-job | 16personalities | Online MBTI clones |
|-----------|----------------|-----------------|--------------------|
| Runs locally, answers stay on device | ✅ | ❌ | ❌ |
| Chinese & English bilingual report | ✅ | Partial | ❌ |
| Three depth levels (70/93/144) | ✅ | ❌ | ❌ |
| Team aggregation report | ✅ | ❌ | ❌ |
| Clarity index + Top-3 similar types | ✅ | ❌ | Rare |
| Professional PDF output | ✅ | Paywall | ❌ |
| Zero dependency core | ✅ | — | — |

---

### 🚀 Workflows

| Workflow | Scenario | Trigger |
|----------|----------|---------|
| Personal assessment | Individual wants to know their type & career fit | Say "MBTI" / "测一下MBTI" to your agent, or run the CLI |
| Team analysis | Team lead wants a team profile from members' results | Say "团队分析 / team MBTI", or run `team_pipeline.py` |
| Resume & retake | Paused mid-test, coming back later | Reopen quiz.html — progress auto-restored |

**Interaction modes** (stacked on personal assessment):

| Mode | Best for | How it works |
|------|----------|--------------|
| Card mode | Chatting with an AI agent | Questions rendered as clickable option cards |
| Conversational | Plain-text hosts | One question per message, reply A/B |
| Web mode | Long tests, teams, desktop | Generated quiz.html with autosave, EN/中文 toggle, one-click answer copy-back |

---

### ⚙️ Technical Specs

| Item | Description |
|------|-------------|
| Type | AI Agent Skill + standalone Python CLI |
| Dependencies | None for core (Python 3.9+ stdlib); optional `weasyprint` / `reportlab` |
| Compatible environments | macOS / Linux / Windows with Python 3.9+; headless PDF needs Chrome or Edge |
| File structure | `data/` (question bank, 16-type profiles, career mapping) + `scripts/` (4 CLI tools) + `references/` |
| Input | Answer JSON (web page export, card mode, or manual) |
| Output | Bilingual PDF report (personal / team), scoring result JSON |
| Languages | 中文 / English (questions, reports, UI) |
| Version | 1.1.1 |
| License | MIT |

---

### 🛠️ Quick Start

**1. Install**

```bash
git clone https://github.com/muippt/mu-mbti-job.git ~/.claude/skills/mu-mbti-job
```

> Other agents may use their own skill directory or a project-level `.claude/skills/mu-mbti-job`.

**2. Verify**

Restart your agent, then:

```
List my available skills
```

**3. Run**

```
I'd like to take an MBTI test for career insights — please use mu-mbti-job.
```

Or invoke a specific workflow:

```
Help me run a team MBTI analysis for my 5 team members.
```

```
Generate a quiz page for the 144-question pro version, in English.
```

Standalone CLI (no agent needed):

```bash
python3 scripts/build_quiz_page.py --version quick -o quiz.html   # generate quiz
python3 scripts/score.py answers.json -o result.json              # score
python3 scripts/generate_report.py result.json -o report.pdf      # PDF
python3 scripts/team_pipeline.py ./team_answers/ -o team.pdf      # team mode
```

---

### 🔒 Security & Privacy

- **All local, all the time** — the quiz page is a single static HTML file; scoring and PDF generation are offline scripts
- **No telemetry, no accounts, no data collection** — nothing is uploaded anywhere
- **Answers are yours** — plain JSON files you can inspect, keep, or delete

> ⚠️ Assessment results are for self-awareness reference only. MBTI is a typology tool, not a clinical instrument, and must not be used for hiring, promotion, or performance decisions.

---

### ⭐ Star History

If this tool helps you or your team, a star ⭐ would be greatly appreciated — it helps more people find a privacy-respecting MBTI assessment.

[View on Star History](https://www.star-history.com/?repos=muippt%2Fmu-mbti-job&type=date) — chart will appear once stars accumulate.

> Three depth levels, bilingual PDF reports, team mode — all offline.

---

### 👤 About the Author

🎓 Signatory Author of Tsinghua University Press / 2026 Dangdang Influential Author / AI & Large Model Business HR Specialist at a Leading Tech Company / National Level-1 HR Manager / Level-2 Psychological Counselor / Self-taught Designer

📚 Author of [*Visual Team Management*](https://item.m.jd.com/product/14547345.html). Clients include ByteDance, Tencent, Baidu, China Mobile, SMG, BOE…

💡 [WeChat Official Account](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [Xiaohongshu](https://xhslink.com/m/ESxtgUNMdl): muippt

### 📄 License & Acknowledgments

[MIT](LICENSE) © 2026 muippt

- Question bank dimension structure references the MBTI Form M item distribution (E/I 21, S/N 26, T/F 24, J/P 22 for the standard version)
- Inspired by open-source MBTI projects and the desire for a privacy-first alternative

> Note: Much of this project was co-created with AI assistance. If you believe your work has been used without proper attribution, please open an issue.
