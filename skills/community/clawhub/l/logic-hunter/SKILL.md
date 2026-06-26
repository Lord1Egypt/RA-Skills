---
name: logic-hunter
description: Hard-core logic verification and evidence tracing tool based on the "Golden Triangle" knowledge mining framework
tags: [research, logic-check, evidence-weighting, red-teaming, fact-verification]
---

# 🛠️ SKILL: Logic Hunter — Golden Triangle Analysis

## 1. Core Principles

You are not collecting information — you are **hunting for truth**.

- **No Single Evidence**: Arguments without cross-verification get weight 0.1
- **Presumption of Doubt**: Conclusions that cannot be traced to primary sources must be labeled as [Logical Hypothesis]

---

## 2. Reasoning Pipeline

1. **Semantic Denoising**: Parse user input, identify core variables, remove adjective misdirection
2. **Weighted Retrieval**: Call search tools to retrieve primary sources (papers, financial reports, government documents)
3. **Confidence Scoring**: Pass data to `logic_engine.py` for confidence calculation
4. **Red Team Challenge**: Simulate opponent role to find "survivor bias" or "reverse causality" in current evidence chain

---

## 3. Mathematical Evaluation Formula

Must strictly follow the scoring model in `logic_engine.py`:

$$C = \frac{\sum (R \times S)}{E}$$

| Symbol | Meaning | Description |
|--------|---------|-------------|
| **R (Reliability)** | Source Grade | Weight of primary/secondary/tertiary sources |
| **S (Support)** | Independent Cross-Evidence Count | Number of independent sources |
| **E (Entropy)** | Logical Risk Entropy | Risk factors like stakeholder bias, semantic drift |

---

## 4. Source Grade Definitions

| Grade | Type | R Value | Examples |
|-------|------|---------|----------|
| **primary** | Primary Source | 1.0 | Official documents, academic papers, original protocols, financial reports |
| **secondary** | Secondary Source | 0.6 | Mainstream in-depth reporting, professional analysis firms |
| **tertiary** | Tertiary Source | 0.2 | Social media, blogs, rumors |
| **unknown** | Unknown Source | 0.05 | Untraceable content |

---

## 5. Output Constraints

Output must follow [One-Page PPT] style — no fluff allowed.

### Standard Output Format

```
🎯 Core Conclusion
[One-sentence conclusion with confidence level]

📊 Evidence Weight
| Source Type | Count | Weight |
|-------------|-------|--------|
| primary     | X     | X.X    |
| secondary   | Y     | Y.Y    |

🔴 Red Team Attack Points
- [Vulnerability 1]
- [Vulnerability 2]

⚠️ Risk Notice
[Logical entropy factor explanation]
```

---

## 6. Trigger Conditions

Activate when user asks questions like:

- "Is this true?" / "How to verify this claim?"
- "Analyze the credibility of this viewpoint"
- "How much evidence supports this conclusion?"
- "Research/verify/investigate [topic]"
- "Deep analysis of [event/claim]"

---

## 7. Tool Invocation

### Available Tools

| Tool | Purpose |
|------|---------|
| `web_search` | Search primary sources |
| `tavily-search` | AI-optimized search |
| `deep-research-pro` | Multi-source deep research |
| `logic_engine.py` | Confidence calculation |

### Invocation Logic

1. Use `web_search` or `tavily-search` to retrieve primary sources
2. Classify search results by source type (primary/secondary/tertiary)
3. Call `logic_engine.py` to calculate confidence
4. Execute red team attack to identify vulnerabilities
5. Output standard format report

---

## 8. Example

### Input
> "Someone says AI will replace all programmers by 2030. Is this credible?"

### Processing Flow
1. Search: AI replace programmers 2030 prediction source
2. Classify sources: Identify which are research reports, media articles, social media
3. Calculate confidence: Call logic_engine.py
4. Red team attack: Find survivor bias, reverse causality

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

---

*Created for Elatia · 2026-03-02*
