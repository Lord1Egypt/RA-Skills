# X.com Investment Analysis Methodology Replication Skill

## Overview

This Skill completely replicates the investment analysis framework of **@jukan05** (GF Securities overseas electronics analyst, 150K+ X platform followers), generating **"as if written by Jukan05 himself"** structured analysis reports for any stock, industry, or market.

### Core Philosophy (Corrected in v4.0)
> **"First identify fast-growing trends, then find the most beneficiary segment within the trend."**
> 
> - **Trend identification** = Starting point (Is this trend big enough? Is it still early?)
> - **Bottleneck positioning** = Screening method (The most beneficiary segment is often the bottleneck)
> - **Technical verification** = Core metrics (yield/lead time/capacity/LTA)
> - **Source rating** = Credibility judgment (S/A/B/C/D five levels)
> - **Execution & risk control** = Jukan's style (concentrated but not gambling, public acknowledgement of mistakes)

---

## Usage

### Trigger Methods
Enter any of the following commands in conversation:
```
Analyze [target] using Jukan's method
How would Jukan view [target]?
Analyze [industry/market] in Jukan's style
```

### Execution Flow (AI automatically completes)
1. **Identify target** → Load Jukan's historical views (if available)
2. **Trend identification** → Search online to answer: Is the trend big enough? Is it still early?
3. **Bottleneck positioning** → Find the most beneficiary segment in the trend
4. **Technical verification** → Get latest data on yield/lead time/capacity/LTA
5. **Source rating** → Cite sources according to S/A/B/C/D levels
6. **Output report** → Jukan style (technical details + disclaimer)

---

## Parameters

This Skill is a **methodology instruction set** with no command-line parameters. The AI automatically executes analysis according to the detailed instructions in `SKILL.md`.

### Supported Target Types
| Type | Examples | Handling |
|------|---------|----------|
| **Stocks (analyzed by Jukan)** | SK Hynix, Samsung, NVIDIA | Load `references/jukan_views/*.md` and cite historical views |
| **Stocks (not analyzed by Jukan)** | Tesla, Tencent, CATL | Derive analysis using Jukan's framework |
| **Industries/Themes** | HBM/memory, advanced packaging, China localization | Analyze via trend identification → bottleneek positioning |
| **Markets** | Semiconductor cycles, AI compute demand | Macro trend + beneficiary segment analysis |

---

## Input/Output Format

### Input
- **User command**: Natural language (Chinese/English both OK)
- **Data sources**: Real-time web search (market data, news, research reports) + Jukan's historical views (if available)

### Output Structure (Jukan Style)
```
[Opening] FWIW / FYI style introduction
  ↓
[Trend identification] What is this trend, is it big enough, is it still early?
  ↓
[Bottleneck positioning] Why is this target the most beneficiary segment?
  ↓
[Technical verification] Yield/lead time/capacity/LTA data (precise numbers)
  ↓
[Source citation] List cited sources according to S/A/B/C/D rating
  ↓
[Target positioning] Zone A/B/C/D + Jukan-style recommendation
  ↓
[Execution advice] Position timing, position sizing, stop-loss signals
  ↓
[Disclaimer] Not investment advice | DYODD
```

### Output Format Options
| Format | Trigger | Description |
|--------|---------|-------------|
| **Conversation reply** | Default | Output Jukan-style analysis directly in conversation |
| **Word document** | User requests "generate report" or "save as document" | Call `scripts/analyze.py` to generate `.docx` |

---

## Dependencies

### Python Dependencies (for generating Word reports)
```bash
pip install python-docx
```

### Web Search Tools (choose any one)
| Tool | Purpose | Priority |
|------|---------|----------|
| `web-tools` Skill | Web Search + Fetch | Recommended |
| `westock-data` Skill | Financial data query | Recommended (if available) |
| `WebSearch` + `WebFetch` | Built-in tools (when no Skill available) | Alternative |

### Optional: Jukan's Historical Tweet Data
- Place at `jukan05_data/jukan05_tweets.csv` (2,454 tweets)
- Used to extract historical views to `references/jukan_views/*.md`
- **Not required** — Even without it, the Skill can still analyze any target using Jukan's framework

---

## Notes

### 1. Not Investment Advice
- Jukan adds `Not investment advice | DYODD` to every analysis
- **You must do the same** — Every analysis must end with a disclaimer

### 2. Distinguish Facts from Opinions
- Jukan's opinions: Use "he thinks" or "Jukan-style analysis indicates"
- Facts: Use "data shows" or "financial reports confirm"

### 3. Acknowledge Blind Spots
- If certain data cannot be obtained (e.g., yield rate of private companies), explicitly state "unable to verify, requires channel check"

### 4. Avoid Overconfidence
- Jukan publicly acknowledges mistakes (Marvell/LG Innotek cases)
- Your analysis should also leave room for correction

### 5. Focus on Semiconductors/AI
- 90% of Jukan's content is in this area; when analyzing other industries, note:
  > "Jukan has limited coverage in this field; the following analysis is a derivative application of his methodology"

### 6. Cookie Expiration (if scraping latest tweets)
- X.com cookies typically valid for **2-3 months**
- After expiration, re-export and update `jukan05_data/x_cookies.json`
- Refer to `x-scraper-cookie` Skill's cookie management process

---

## File Structure

```
x-investment-strategy-analyzer/
├── SKILL.md                          # Core instruction file (five-layer analysis method)
├── README_zh.md                     # Chinese documentation
├── README_en.md                     # English documentation (this file)
├── scripts/
│   └── analyze.py                  # Report generator (Word output)
└── references/
    ├── jukan_framework_universal.md  # Detailed five-layer method
    ├── jukan_style_guide.md         # Jukan language style guide (Few-shot)
    └── jukan_views/                # Jukan's historical views library (optional)
        ├── sk_hynix.md
        ├── samsung.md
        ├── nvidia.md
        ├── tsmc.md
        ├── intel.md
        ├── memory_hbm.md
        ├── china_semiconductor.md
        └── foundry.md
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-07-01 | Initial version (generic five-dimension framework) |
| v2.0 | 2026-07-01 | Inject Jukan knowledge base + style guide |
| v3.0 | 2026-07-01 | Universal modification (support any target) |
| **v4.0** | **2026-07-02** | **Correct core philosophy: "trend identification first" not "bottleneck theory"** |

---

## 10 English Tags

```
X.com, Twitter, investment analysis, semiconductor, AI, trend identification, 
supply chain bottleneek, growth stock, Jukan05, financial framework
```
