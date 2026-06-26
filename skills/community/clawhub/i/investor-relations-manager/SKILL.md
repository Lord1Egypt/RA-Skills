---
name: investor-relations-manager
description: AI-powered Investor Relations Manager - automated video generation for earnings reports, financial updates, and stakeholder communications
tags: [investor-relations, financial-reporting, earnings, stakeholder-communications, video-generation, remotion, openai, tts, ai-video, corporate-communications]
---

# Investor Relations Manager Skill

AI-powered Investor Relations Manager that transforms financial data and business updates into professional video presentations for investors, stakeholders, and the financial community.

## Installation

### Step 1: Install the Skill

```bash
clawhub install investor-relations-manager
```

### Step 2: Clone & Setup the Project

```bash
# Clone to standard location
git clone https://github.com/ZhenRobotics/openclaw-investor-relations-manager.git ~/openclaw-investor-relations-manager
cd ~/openclaw-investor-relations-manager

# Install dependencies
npm install

# Configure API key
echo 'OPENAI_API_KEY="sk-your-key-here"' > .env
```

### Step 3: Verify Installation

```bash
cd ~/openclaw-investor-relations-manager
./agents/ir-cli.sh help
```

---

## Usage

### When to Use This Skill

**AUTO-TRIGGER** when user's message contains:

- Keywords: `investor relations`, `earnings report`, `quarterly report`, `financial update`, `stakeholder communication`, `IR video`, `财报`, `业绩发布`, `投资者关系`
- Provides financial data (revenue, profit, growth percentages, user metrics)
- Mentions quarterly/annual reports (Q1, Q2, Q3, Q4, annual)
- Requests professional business video for investors

**TRIGGER EXAMPLES** (always use this skill for these):
- "Generate Q3 earnings report video"
- "Create investor update: revenue grew 45% to $2.3B"
- "Make stakeholder communication video for quarterly results"
- "生成Q3季度财报视频"
- "制作投资者业绩更新视频"

**DO NOT USE** when:
- General marketing videos (use video-generator skill)
- Entertainment or social media content
- Internal training videos

---

## Core Features

Complete IR video generation pipeline:

- **TTS Generation** - Professional business voice (default: alloy, neutral and clear)
- **Timestamp Extraction** - OpenAI Whisper API for precise segmentation
- **Financial Scene Detection** - Intelligent recognition of metrics, growth indicators, KPIs
- **Professional Rendering** - Corporate-style visuals with financial green/blue color scheme
- **Background Video Support** - Custom backgrounds with opacity control
- **Data Visualization** - Highlight key financial metrics and performance indicators

---

## Agent Usage Guide

### Important Notes

**CRITICAL**: Use the existing project directory. Do NOT create new projects.

Project location:
- Standard install: `~/openclaw-investor-relations-manager/`
- Or detect: Ask user for project location on first use

### Primary Command: Generate IR Video

When user requests investor relations video generation, execute:

```bash
# Method 1: CLI (Recommended)
cd ~/openclaw-investor-relations-manager && ./agents/ir-cli.sh generate "Q3 revenue grew 45% to $2.3B. Net profit increased 60% to $35M."

# Method 2: Full pipeline script
cd ~/openclaw-investor-relations-manager && ./scripts/script-to-video.sh scripts/q3-earnings.txt \
  --voice alloy --speed 1.0

# Method 3: With background video
cd ~/openclaw-investor-relations-manager && ./scripts/script-to-video.sh scripts/annual-report.txt \
  --bg-video public/corporate-bg.mp4 \
  --bg-opacity 0.3
```

**Example**:

User says: "Generate Q3 earnings video: Revenue $2.3B, up 45%. Profit $35M, up 60%."

Execute:
```bash
cd ~/openclaw-investor-relations-manager && ./agents/ir-cli.sh generate "Q3 earnings report. Revenue reached 2.3 billion dollars, up 45%. Net profit 35 million dollars, up 60%. Strong quarter performance."
```

### Output Location

Generated video saved at: `~/openclaw-investor-relations-manager/out/generated.mp4`

---

## Configuration Options

### Voice Selection
- `alloy` - Neutral, professional (Recommended for IR)
- `echo` - Clear and authoritative
- `onyx` - Deep, executive-style

### Speed
- Range: 0.25 - 4.0
- Recommended: 1.0 (professional pace for investor presentations)
- Default: 1.0

### Video Style
- Professional corporate presentation (default)
- Quarterly earnings report
- Annual shareholder update
- Product launch / business milestone

---

## Scene Types (IR-Optimized)

System automatically detects 6 scene types optimized for financial content:

| Type | Effect | Trigger Condition | IR Use Case |
|------|--------|-------------------|-------------|
| **title** | Professional opening | First segment | "Q3 Earnings Report" |
| **emphasis** | Highlight metrics | Growth %, financial numbers | "Revenue +45%", "$2.3B" |
| **circle** | KPI highlight | Revenue, profit, users | "500M users", "Net profit" |
| **content** | Regular business update | Quarterly/period mentions | "Q3 performance" |
| **pain** | Challenges/concerns | Risk, challenge keywords | "Market challenges" |
| **end** | Professional closing | Last segment | "Thank you, investors" |

---

## Financial Metric Detection

The system intelligently recognizes:

- **Growth indicators**: 增长, 提升, 上涨, growth, increase, %
- **Financial metrics**: 营收, 收入, 利润, 净利润, revenue, profit, earnings
- **User metrics**: 用户, 客户, users, customers
- **Time periods**: Q1, Q2, Q3, Q4, 季度, quarter, annual
- **Challenges**: 挑战, 风险, challenge, risk, concern

---

## Cost Estimation

Per 60-second IR video: **~$0.012** (about 1 cent):

- OpenAI TTS: ~$0.004
- OpenAI Whisper: ~$0.008
- Remotion rendering: Free (local)

---

## Usage Examples

### Example 1: Q3 Earnings Report

User: "Generate Q3 earnings video: Revenue $2.3B up 45%, profit $35M up 60%, 5M users"

Agent executes:
```bash
cd ~/openclaw-investor-relations-manager && ./agents/ir-cli.sh generate "Q3 earnings report. Revenue reached 2.3 billion dollars, up 45%. Net profit 35 million dollars, up 60%. User base reached 5 million. Strongest quarter in company history."
```

Output: `~/openclaw-investor-relations-manager/out/generated.mp4` (45-60 seconds, professional IR video)

### Example 2: Annual Shareholder Update

User: "Create annual report video: 2024 revenue $800M, up 120%, expanded to 200 enterprise customers"

Agent:
```bash
cd ~/openclaw-investor-relations-manager && ./scripts/script-to-video.sh scripts/annual-report.txt \
  --voice alloy --speed 1.0
```

### Example 3: Product Launch IR Video

User: "New AI product launch, expected $50M annual revenue"

Agent creates optimized script and executes:
```bash
cd ~/openclaw-investor-relations-manager && ./agents/ir-cli.sh generate "Major product launch. AI-powered enterprise solution now live. Expected annual revenue contribution 50 million dollars. 50 enterprise customers pre-committed. New growth phase begins."
```

---

## Video Specifications

- **Resolution**: 1080 x 1920 (Portrait) or 1920 x 1080 (Landscape - configurable)
- **Frame Rate**: 30 fps
- **Format**: MP4 (H.264 + AAC)
- **Style**: Professional corporate with financial color scheme
- **Duration**: Auto-calculated based on content (typically 30-90 seconds)

---

## Color Scheme

Professional financial/corporate colors:

- **Primary**: Corporate Blue (#0078D7)
- **Accent**: Financial Green (#00A86B)
- **Background**: Professional Dark Blue-Grey (#0F1419)
- **Text**: White (#FFFFFF) with subtle shadows

---

## Troubleshooting

### Issue 1: Project Not Found

**Error**: `bash: ~/openclaw-investor-relations-manager/...: No such file or directory`

**Solution**:
```bash
git clone https://github.com/ZhenRobotics/openclaw-investor-relations-manager.git ~/openclaw-investor-relations-manager
cd ~/openclaw-investor-relations-manager && npm install
```

### Issue 2: API Key Error

**Solution**:
```bash
cd ~/openclaw-investor-relations-manager
echo 'OPENAI_API_KEY="sk-your-key-here"' > .env
```

### Issue 3: Data Accuracy Concerns

**Important**: Always verify financial data accuracy before using in official communications. This tool is for presentation generation only - data accuracy is the user's responsibility.

---

## Full Documentation

- **GitHub**: https://github.com/ZhenRobotics/openclaw-investor-relations-manager
- **Quick Start**: `~/openclaw-investor-relations-manager/QUICKSTART.md`
- **README**: `~/openclaw-investor-relations-manager/README.md`

---

## Important Notes

1. **Data Accuracy**: Always verify financial data before official release
2. **Compliance**: Ensure content complies with financial disclosure regulations
3. **API Configuration**: Valid `OPENAI_API_KEY` required (use `.env` file)
4. **Professional Voice**: Default voice is "alloy" (neutral, professional)
5. **Review Required**: Always review generated videos before investor distribution

---

## Agent Behavior Guidelines

When using this skill, agents should:

**DO**:
- Verify the data provided by user before generating
- Use professional, formal language for IR content
- Highlight key financial metrics (revenue, profit, growth %)
- Ask for clarification on ambiguous numbers
- Remind users to review for compliance

**DON'T**:
- Make up financial data
- Use casual or entertainment-style narration
- Ignore data accuracy concerns
- Skip verification of critical numbers

---

## Tech Stack

- **Remotion**: React-based video generation framework
- **OpenAI TTS**: Text-to-speech API (professional voices)
- **OpenAI Whisper**: Speech recognition API
- **TypeScript**: Type-safe development
- **React**: UI component framework
- **Node.js**: Runtime environment

---

## Version History

### v1.0.0 (2026-03-07)
- Initial release of Investor Relations Manager
- Professional corporate visual style
- Financial metric detection
- IR-optimized scene types
- Professional color scheme (corporate blue/financial green)
- Example IR scripts (Q3 earnings, annual report, product launch)

---

**Project Status**: Production Ready for Investor Relations

**License**: MIT

**Author**: @ZhenStaff

**Support**: https://github.com/ZhenRobotics/openclaw-investor-relations-manager/issues

**ClawHub**: https://clawhub.ai/ZhenStaff/investor-relations-manager
