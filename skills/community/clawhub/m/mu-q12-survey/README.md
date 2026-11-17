<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/default-banner.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/default-banner.png">
    <img alt="mu-q12-survey" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 📊 mu-q12-survey · Q12敬业度调研助手

> AI-powered employee engagement survey assistant based on Gallup Q12 — from questionnaire design to result interpretation to 90-day improvement plans.

**English** | [中文](README_CN.md) | [🌐 Landing Page](https://muippt.github.io/mu-q12-survey/)

[![WeChat](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![Xiaohongshu](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![Book](https://img.shields.io/badge/Book-Visual%20Team%20Management-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skillhub](https://img.shields.io/badge/mu--skillhub-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-q12-survey)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-q12-survey)](https://github.com/muippt/mu-q12-survey/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-q12-survey)](https://github.com/muippt/mu-q12-survey/stargazers)

### 💡 Usage Examples

- **📋 Design a Q12 Survey** — "Help me create an engagement survey for my 30-person engineering team" → Get a customized questionnaire with standard Q12 + team-specific add-on questions
- **📈 Interpret Survey Results** — "Here are my Q1-Q12 average scores" → Get a full diagnostic report with engagement distribution, weak areas, and high-risk combinations
- **💡 Get Improvement Advice** — "Q4 and Q5 are low, what should I do?" → Receive prioritized quick-win and mid-term actions linked to specific Q12 items
- **🗺️ 90-Day Improvement Plan** — "Team engagement is only 12%, I need a plan" → Get a structured 90-day action plan with milestones and expected outcomes
- **🔍 Diagnose High-Risk Signals** — "Multiple scores below 2.5" → Identify dangerous combinations like Q1+Q4+Q5 (manager capability crisis) and get targeted interventions
- **📊 Benchmark Comparison** — "How does my team compare?" — Compare against Gallup global (23%) and China regional (17-18%) engagement benchmarks
- **🎯 Focused Diagnosis** — "I suspect management issues" → Get a focused analysis using the relevant Q12 subset (Q4, Q5, Q6, Q11) instead of the full survey

### ✨ Core Highlights

#### Complete Gallup Q12 Framework

All 12 original Gallup Q12 questions with management implications for each, organized into the four-level "climbing model":

| Level | Theme | Questions |
|-------|-------|-----------|
| Base Camp | Basic Needs | Q1 (expectations), Q2 (materials/equipment) |
| Camp 1 | Individual Contribution | Q3 (strengths), Q4 (recognition), Q5 (care), Q6 (development) |
| Camp 2 | Team Belonging | Q7 (opinions), Q8 (mission), Q9 (quality), Q10 (best friend) |
| Camp 3 | Mutual Growth | Q11 (progress feedback), Q12 (learning/growth) |

#### Three Survey Versions for Different Scenarios

| Version | Questions | Best For |
|---------|-----------|----------|
| Standard (Full) | All 12 Q12 items | Annual benchmarking, first-time diagnosis |
| Lite (8 items) | Q1, Q2, Q3, Q4, Q5, Q8, Q11, Q12 | Quarterly pulse checks |
| Focused (variable) | Topic-specific subsets | Targeted diagnosis of known issues |

#### Result Interpretation Engine

Three-tier engagement classification with management signals:

- **Engaged** (avg ≥ 4.0, no item ≤ 2.0) — ~17-20% in China
- **Not Engaged** (avg 2.5-3.9) — ~60-65% in China
- **Actively Disengaged** (avg < 2.5 or multiple items ≤ 2.0) — ~15-20% in China

Plus **high-risk combination detection**: Q1+Q4+Q5 (manager crisis), Q3+Q6+Q12 (career path blockage), Q7+Q8 (disengagement), Q9+Q10 (team cohesion collapse).

#### Actionable Improvement Library

Every Q12 item has pre-built **quick-win** (within 1 week) and **mid-term** (1-3 months) actions. No generic advice — every recommendation is linked to specific low-scoring items.

### 📌 Comparison

| Feature | mu-q12-survey | Gallup Official Tools | Generic Survey Platforms |
|---------|---------------|----------------------|--------------------------|
| Q12 Full Framework | ✅ All 12 questions + management implications | ✅ Original source | ❌ Custom questions only |
| Survey Design | ✅ 3 versions (standard/lite/focused) + custom add-ons | ✅ Standardized | ✅ Fully custom |
| Result Interpretation | ✅ Three-tier + high-risk combinations + benchmark | ✅ Professional dashboard | ⚠️ Basic charts only |
| Improvement Actions | ✅ Per-item quick-win + mid-term + 90-day plan | ⚠️ Paid consulting | ❌ None |
| AI-Powered | ✅ Conversational, adaptive | ❌ Static reports | ⚠️ Template-based |
| Cost | ✅ Free (open source) | ❌ Expensive license | ⚠️ Freemium |
| Privacy | ✅ Fully local, no data collection | ⚠️ Cloud-based | ⚠️ Cloud-based |

### 🚀 Workflows

| Workflow | Scenario | Trigger |
|----------|----------|---------|
| Questionnaire Design | Need to create an engagement survey | "Help me design a Q12 survey" / "I want to do an engagement survey" |
| Result Interpretation | Have survey data, need analysis | "Interpret my survey results" / "I got the data" |
| Improvement Advice | Know the weak areas, need actions | "How to improve team engagement" / "Low scores, what to do" |
| Q12 Framework Intro | Want to understand Gallup Q12 | "What is Q12" / "Tell me about Gallup" |

### ⚙️ Technical Specs

| Item | Description |
|------|-------------|
| Type | AI Prompt Skill (knowledge-based, no code) |
| Framework | Gallup Q12 Engagement Survey |
| Compatibility | Any AI assistant that supports markdown prompts (ChatGPT, Claude, Gemini, etc.) |
| Data Source | Gallup public research (12 industries, 24 companies, 100,000+ employees) |
| Benchmarks | Global (23%), Asia-Pacific (17%), China (17-18%), Tech industry (~22-25%) |
| Languages | English + Chinese |
| Dependencies | None (pure knowledge content) |
| Output | Customized questionnaires, diagnostic reports, 90-day improvement plans |

### 🛠️ Quick Start

1. **Download the SKILL.md** file from this repository.

2. **Load it into your AI assistant** (ChatGPT, Claude, Gemini, or any markdown-aware AI tool):
   ```
   # Simply paste the content of SKILL.md as a system prompt or knowledge base document.
   ```

3. **Start asking!** Try: *"Help me design a Q12 engagement survey for my 20-person sales team"*

### 🔒 Security & Privacy

- **100% Local** — No data is sent to any server. The skill is a pure knowledge document.
- **No Telemetry** — Zero tracking, zero analytics, zero data collection.
- **No Dependencies** — No npm packages, no API keys, no external services required.
- **Survey Data Stays Yours** — The skill only provides methodology; your actual survey data never leaves your environment.

### ⭐ Star History

If this tool helps your team, please consider giving it a star ⭐

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-q12-survey&type=date)

> Open-source Gallup Q12 engagement survey assistant — from questionnaire to 90-day improvement plan, all in one skill.

### 👤 About the Author

🎓 Signatory Author of Tsinghua University Press / 2026 Dangdang Influential Author / AI & Large Model Business HR Specialist at a Leading Tech Company / National Level-1 HR Manager / Level-2 Psychological Counselor / Self-taught Designer

📚 Author of [*Visual Team Management*](https://item.m.jd.com/product/14547345.html). Clients include ByteDance, Tencent, Baidu, China Mobile, SMG, BOE…

💡 [WeChat Official Account](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [Xiaohongshu](https://xhslink.com/m/ESxtgUNMdl): muippt

### 📄 License & Acknowledgments

[MIT](LICENSE) © 2026 muippt

This project is based on the Gallup Q12 employee engagement framework. Gallup Q12 is a registered trademark of Gallup, Inc. This project is an independent application of the publicly available Q12 research framework and is not affiliated with or endorsed by Gallup.

> Note: Much of this project was co-created with AI assistance. If you believe your work has been used without proper attribution, please open an issue.
