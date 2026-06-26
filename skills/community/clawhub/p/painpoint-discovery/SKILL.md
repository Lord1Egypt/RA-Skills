---
name: painpoint-discovery
description: Painpoint discovery expert. Helps users discover, analyze, and evaluate startup painpoints in specific domains. Use when user says "find painpoints in X", "analyze opportunities in X", "startup research".
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [], "tools": ["browser"] },
        "install": [],
      },
  }
---

# Painpoint Discovery Expert

## Use Cases

Use when users want to explore startup opportunities in a specific domain:
- "Find painpoints in the weight loss domain"
- "Analyze opportunities in remote work"
- "I want to build something in pet care, what painpoints are worth solving"

## Core Capabilities

### 1. Web Research & Mining
- Search social media, forums, reviews for user complaints
- Analyze discussion volume around related topics
- Identify high-frequency problems and frustrations

### 2. Painpoint Structuring
Each painpoint includes:
- **Scenario**: When/where does this problem occur
- **Problem**: What specifically is the frustration
- **Target Audience**: Who experiences this painpoint
- **Frequency**: How often does it occur
- **Existing Solutions**: Current approaches and why they fall short

### 3. Solution Recommendations
Based on painpoint type, recommend:
- 📱 **App/Mini-program**: High-frequency, lightweight, mobile scenarios
- 💻 **SaaS/Tool**: Workflow, B2B, requires ongoing use
- 📦 **Hardware**: Physical interaction, sensors, dedicated devices
- 📚 **Content/Education**: Knowledge gaps, skill learning
- 🤝 **Service/Platform**: Connecting supply/demand, matching problems

### 4. Business Value Assessment
- **Market Size**: Potential users × willingness to pay
- **Competition**: Number and quality of existing players
- **Entry Barrier**: Technical/capital/resource requirements
- **Willingness to Pay**: Will users actually spend money
- **Recommendation**: ⭐⭐⭐⭐⭐ (1-5 stars)

## Output Formats

### Mode 1: Comprehensive Report (Default)

```markdown
# [Domain] Painpoint Analysis Report

## Research Sources
- Search keywords: [...]
- Data sources: [social media/forums/reviews/news]
- Research date: [date]

## Painpoint 1: [Name]
[...]

## Painpoint Knowledge Graph
[...]

## Next Steps & Recommendations
[...]
```

### Mode 2: AhaPoints Format (`--ahapoints`)

Generate independent AhaPoint reports for each painpoint:

```
ahapoints-protocol/points/
├── YYYYMMDD-HHMM-PAIN-[Title1].md
├── YYYYMMDD-HHMM-PAIN-[Title2].md
└── YYYYMMDD-HHMM-INNO-[Title3].md
```

Uses AhaPoints Protocol v1.0 template:
1. Point Type
2. One-liner Description
3. Scenario Story
4. Why It Matters
5. Potential Solution Directions
6. Validation Methods
7. Metadata

**Priority**: Timestamp on each report serves as priority proof

## Workflow (Browser Mode - No API Required)

1. **Confirm Domain**: Ask user which domain/topic to explore
2. **Open Search Engine**:
   - `browser.navigate("https://www.google.com/search?q=[domain]+problems+OR+frustration+OR+complaints")`
3. **Capture Search Results**:
   - `browser.snapshot()` → Extract titles and summaries
   - Record high-quality result links
4. **Deep Scraping** (Optional):
   - `browser.navigate(link)` Open specific pages
   - `browser.snapshot()` → Extract detailed content
5. **Structured Output**: Compile into report format
6. **Optional Deep Dive**: User can select a painpoint for further research

## Workflow (API Mode - If Brave Configured)

1. **Confirm Domain**
2. **web_search** for complaints and discussions
3. **web_fetch** specific pages for content analysis
4. **Structured Output**

## Important Notes

- Prioritize **specific complaints**, not vague "I want X"
- Distinguish **real painpoints** (willing to pay) from **pseudo-needs** (just talking)
- Remind users: research results need real-world validation
- Encourage users to supplement with their own experiences
- **Browser mode is slower** - recommend 3-5 search keywords max
