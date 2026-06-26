# Painpoint Discovery Skill

## 📁 File Structure

```
painpoint-discovery/
├── SKILL.md           # Skill definition and usage guide
├── agent-config.md    # Standalone subagent configuration
├── example-report.md  # Example output report
├── runner.md          # Execution flow and checklist
└── README.md          # This file
```

## 🚀 Usage

### Mode 1: Skill Mode (Quick)

User says:
> "Find painpoints in the weight loss domain"

OpenClaw automatically calls this skill, executes quick research (3-5 searches), outputs structured painpoint analysis.

**Best for**:
- Quick domain exploration
- Initial painpoint landscape understanding
- Single-session completion

---

### Mode 2: Subagent Mode (Deep Research)

User says:
> "Do deep research on remote work painpoints, I want a detailed report"

OpenClaw spawns independent subagent, executes deep research (10+ searches, 30 min), generates complete report file.

**Best for**:
- Comprehensive, in-depth analysis needed
- Saveable report output required
- Knowledge graph visualization needed

---

## 📊 Output Contents

Each painpoint analysis includes:
1. **Scenario Description** - When/where it occurs
2. **Core Problem** - What's the本质 issue
3. **Target Audience** - Who experiences it
4. **Existing Solutions & Gaps** - Why it's still unsolved
5. **Solution Recommendations** - App/Hardware/SaaS/Content/Service
6. **Business Value Assessment** - Market/Competition/Barrier/Willingness/Rating

---

## 🎯 Key Advantages

| Feature | Description |
|---------|-------------|
| **Data-Driven** | Based on real web data, not guesswork |
| **Structured** | Consistent format for easy comparison |
| **Actionable** | Each painpoint has MVP ideas and validation methods |
| **Knowledge Graph** | Visualize painpoint relationships |
| **Dual Mode** | Quick explore or deep dive, choose as needed |

---

## 💡 Typical Use Cases

1. **Indie Developers Finding Direction** - "I want a side project, find painpoints in X"
2. **Founders Validating Ideas** - "I have an X idea, is this a real painpoint"
3. **Product Managers Finding Opportunities** - "We're entering X market, any white space"
4. **Investors Doing Research** - "Analyze startup opportunities in X domain"

---

## ⚠️ Important Notes

- Research results need **real-world validation**, don't treat as final conclusions
- Distinguish **real painpoints** (willing to pay) from **pseudo-needs** (just talking)
- Encourage users to supplement with their own experiences
- Business assessments are estimates - actual market research still needed

---

## 📝 Version History

- **v1.0** (2026-03-04) - Initial release
  - Basic painpoint discovery capability
  - Support for skill and subagent dual modes
  - Structured output template

---

## 🔧 Installation

```bash
clawhub install painpoint-discovery
```

---

## 🤝 Contributing

Welcome contributions:
- New research methodologies
- Better output formats
- Domain-specific analysis templates
