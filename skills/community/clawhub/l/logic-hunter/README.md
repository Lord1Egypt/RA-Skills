# Logic Hunter

Hard-core logic verification and evidence溯源 tool based on the "Golden Triangle" knowledge mining framework. **For critical thinking, fact verification, and evidence-weighted analysis.**

## What This Does

**Logic Hunter** helps you verify claims, analyze argument credibility, and uncover hidden logical vulnerabilities. It uses a rigorous mathematical model to score evidence reliability and cross-verification.

### Key Features

- **Golden Triangle Framework** — Three-pillar analysis: Source Reliability (R), Independent Support (S), Logical Entropy (E)
- **Confidence Scoring** — Mathematical formula: C = Σ(R × S) / E
- **Red Team Challenge** — Automatically finds survivor bias, reverse causality, and other logical vulnerabilities
- **Primary Source Priority** — Requires cross-verification from primary sources (papers, official documents, financial reports)
- **One-Page Output** — Clean, actionable report format — no fluff

## When to Use

Use Logic Hunter when you need to:

- Verify a claim's credibility ("Is this true?")
- Analyze argument strength ("How much evidence supports this?")
- Find logical vulnerabilities ("What's wrong with this reasoning?")
- Deep research with evidence weighting ("Research [topic] with source verification")
- Fact-check before making decisions

## Installation

### For OpenClaw / ClawHub Users

If you use [OpenClaw](https://docs.openclaw.ai/) or ClawHub:

- **CLI (if skill is on ClawHub):**  
  `clawhub install logic-hunter`
- **Manual:** Copy this repo (or `SKILL.md`, `logic_engine.py`, and related files) into your OpenClaw workspace skills directory, e.g.  
  `./skills/logic-hunter/`  
  Then reload or restart the runtime.

### For Cursor Users

Place the skill in your project or user skills directory:

- **Project skill:** `.cursor/skills/logic-hunter/`
- **User skill:** See Cursor docs for user-level skills path

Then trigger by describing what you need, e.g.: "Use logic-hunter to verify this claim" or "Analyze the credibility of [statement]".

### For Claude Code Users

Copy the skill files to your Claude Code skills directory:

```bash
# Create the skill directory
mkdir -p ~/.claude/skills/logic-hunter

# Copy the files
cp SKILL.md ~/.claude/skills/logic-hunter/
cp logic_engine.py ~/.claude/skills/logic-hunter/
```

Then use it by typing `/logic-hunter` in Claude Code.

## Output Format

Every analysis produces a standardized one-page report:

```
🎯 Core Conclusion
[One-sentence conclusion with confidence level]

📊 Evidence Weight
| Source Type | Count | Weight |
|-------------|-------|--------|
| primary     | X     | X.X    |
| secondary   | Y     | Y.Y    |
| tertiary    | Z     | Z.Z    |

🔴 Red Team Attack Points
- [Vulnerability 1]
- [Vulnerability 2]

⚠️ Risk Notice
[Logical entropy factor explanation]
```

## Source Grades

| Grade | Type | R Value | Examples |
|-------|------|---------|----------|
| **primary** | Primary Source | 1.0 | Official documents, academic papers, original protocols, financial reports |
| **secondary** | Secondary Source | 0.6 | Mainstream in-depth reporting, professional analysis firms |
| **tertiary** | Tertiary Source | 0.2 | Social media, blogs, rumors |
| **unknown** | Unknown Source | 0.05 | Untraceable content |

## Confidence Formula

$$C = \frac{\sum (R \times S)}{E}$$

- **R (Reliability)**: Source grade weight
- **S (Support)**: Independent cross-evidence count
- **E (Entropy)**: Logical risk factors (stakeholder bias, semantic drift, etc.)

**Interpretation:**
- C > 0.8: High confidence
- C 0.5–0.8: Moderate confidence
- C < 0.5: Low confidence — treat as hypothesis

## Example

### Input
> "Someone says AI will replace all programmers by 2030. Is this credible?"

### Output
```
🎯 Core Conclusion
"AI will replace all programmers by 2030" — Confidence 0.23 (Low)

📊 Evidence Weight
| Source Type | Count | Weight |
|-------------|-------|--------|
| primary     | 0     | 0.0    |
| secondary   | 2     | 1.2    |
| tertiary    | 5     | 1.0    |

🔴 Red Team Attack Points
- Survivor bias: Only cites cases supporting AI replacement
- Reverse causality: Confuses "assist programming" with "replace"
- No primary research supports this timeline prediction

⚠️ Risk Notice
Logical entropy factor E=2.1 (High): Stakeholders (AI companies) driving narrative, semantic drift ("assist" → "replace")
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill instructions |
| `logic_engine.py` | Confidence calculation engine |
| `MANIFEST.json` | Skill metadata and capabilities |
| `tools_schema.json` | Tool invocation schema |
| `TEST_CASES.md` | Test cases and validation |

## Requirements

- Python 3.x (for `logic_engine.py` execution)
- Web search capability (web_search or tavily-search)
- Optional: deep-research-pro for multi-source analysis

## Credits

Created by Elatia with the Golden Triangle knowledge mining framework.

## License

MIT — Use it, modify it, share it.
