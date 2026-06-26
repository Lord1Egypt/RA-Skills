# Bilingual Templates — 中英文术语对照与输出模板

When the user's input language is English, all Agent outputs switch to English. This file provides the English output templates and key term mappings.

## Key Term Glossary

| 中文 | English | Context |
|------|---------|---------|
| 比稿 | Competitive Pitch / Pitch | Agency selection process |
| 竞标 | Bid / Tender | Formal procurement |
| 提案 | Pitch / Proposal | Client presentation |
| 招标 | RFP (Request for Proposal) | Client procurement document |
| 作战卡 | Battle Card | Intake output |
| 隐性信号 | Hidden Signals | Brief subtext analysis |
| 情报层 | Information Engine | Intelligence gathering |
| 策略层 | Strategy Engine | Strategic planning |
| 决策层 | Decision Engine | Decision intelligence |
| 表达层 | Expression Engine | Pitch expression |
| 交付层 | Delivery Engine | Output packaging |
| 问题重构 | Problem Reframing | Three-layer reframing |
| 本质问题 | Essential Problem | Root cause identification |
| 洞察 | Insight | Consumer truth + brand intersection |
| 策略路径 | Strategy Path | Challenge → Insight → Idea → Framework → Impact |
| 风险对冲 | Risk Hedging | Conservative / Balanced / Aggressive versions |
| 决策模式 | Decision Mode | Safety / Political / Aggressive / Procurement |
| 权力图谱 | Power Graph | Stakeholder influence mapping |
| 胜率计算 | Win Probability | Five-dimension scoring |
| 决策模拟 | Decision Simulation | Mock pitch meeting |
| 竞品推演 | Shadow Pitch | Competitor strategy prediction |
| 逻辑空位 | Strategy Gap | Uncontested strategy space |
| 情绪曲线 | Emotion Curve | Pitch emotional rhythm |
| 黄金开场 | Opening Hook | First impression statement |
| Q&A压力训练 | Q&A Red Team | Hostile question preparation |
| 保守版/折中版/激进版 | Conservative / Balanced / Aggressive | Risk hedging versions |
| 决策者/影响者/否决者 | Decider / Influencer / Veto Holder | Stakeholder roles |
| 隐形决策者 | Hidden Decider | Off-table power player |

## English Output Templates

### Battle Card (Intake Agent)

```
Project Battle Card:

Client: {name} | Industry: {industry} | Stage: {Growth/Transition/Crisis/Maintenance}

Objective:
  Type: {Growth/Brand/Transition/Crisis/Maintenance}
  Primary Goal: {one sentence}
  KPI Hints: {hinted KPI directions}

Constraints:
  Budget: {amount or "Flexible"}
  Timeline: Brief received {date} → Deadline {date} → Pitch {date} ({N} working days)
  Channels: {specified channels}
  Special Requirements: {any constraints}

Deliverables: {list}

Hidden Signals:
  - {Signal}: {evidence from Brief} → {implication for strategy}

Competition:
  Estimated Competitors: {number}
  Likely Types: {competitor profiles}
  Our Advantage: {core competitive edge}

Battle Card Summary:
  One-line Strategy: {one sentence}
  Must-Win Dimension: {dimension}
  Avoid Dimension: {dimension}
  Risk Level: {Low/Medium/High}
  Recommended Approach: {Attack/Defend/Differentiate}
```

### Strategy Path (Strategy Agent)

```
Strategy Path:

CHALLENGE
  {What is the market reality? Why is the status quo unsustainable?}

↓ INSIGHT
  {What did we discover that others missed?}

↓ STRATEGIC IDEA
  {One-line strategic proposition — this must be unique to us}

↓ EXECUTION FRAMEWORK
  Phase 1 — Quick Win ({duration}): {core actions}
  Phase 2 — Scale Up ({duration}): {core actions}
  Phase 3 — Sustain ({duration}): {core actions}

↓ EXPECTED IMPACT
  ROI Projection: {range}
  Market Share Target: {target}
  Brand Metrics: {expected changes}
```

### Win Probability Report (Decision Agent)

```
Win Rate Assessment:

Overall Win Rate: {XX}%
Evidence Quality: {High/Medium/Low}

Score Breakdown:
  Strategy Fit: {X}/10
    Evidence: {specific data point from Information/Strategy Agent}
    Evidence Strength: {Strong/Limited/Insufficient}
  Decision Maker Fit: {X}/10
    Evidence: {specific Persona data point}
    Evidence Strength: {Strong/Limited/Insufficient}
  Competitor Differentiation: {X}/10
    Evidence: {Strategy Gap analysis}
    Evidence Strength: {Strong/Limited/Insufficient}
  Execution Credibility: {X}/10
    Evidence: {case studies / team credentials}
    Evidence Strength: {Strong/Limited/Insufficient}
  Relationship & Price: {X}/10
    Evidence: {user-provided info / industry norms}
    Evidence Strength: {Strong/Limited/Insufficient}

Key Risks:
  1. {risk} — Impact: {High/Medium/Low} — Mitigation: {action}
  2. {risk} — Impact: {High/Medium/Low} — Mitigation: {action}

Optimization Roadmap:
  1. {action} → Expected lift: +{X}% (Priority: High)
  2. {action} → Expected lift: +{X}% (Priority: Medium)
```

### Pitch Structure (Expression Agent)

```
Pitch Structure ({total_duration} minutes):

1. Opening Hook ({1-2} min)
   Type: {Anxiety Strike / Data Shock / Question Pierce / Counter-Intuitive / Empathy}
   Hook: {opening statement}
   Key Message: {core message}

2. Problem Reframing ({3-5} min)
   Official Problem: {what the Brief says}
   Surface Problem: {what's behind the Brief}
   Essential Problem: {the real issue} ⭐

3. Insight ({3-5} min)
   Consumer Truth: {insight}
   Brand Connection: {why this brand uniquely}

4. Strategy ({5-8} min)
   Strategic Idea: {one-line proposition}
   Framework: {execution structure}

5. Execution ({5-8} min)
   Timeline + Key Actions + Milestones

6. Expected Impact ({3-5} min)
   ROI + Benchmarks + Risk Controls

7. Risk Management ({2-3} min)
   Proactive risk identification + Safety nets + Plan B triggers

8. Closing ({1-2} min)
   Callback to Opening + One-line Summary + Clear Next Step
```

### Q&A Red Team (Expression Agent)

```
Q&A Red Team — {decision_mode} Mode Optimized

Q: {hostile question}
A: {30-second answer}
   Data Support: {if available}
   Answer Strategy: {intent of this answer}
   Rhythm Type: {Cut-short / Expand / Reverse}

  Cut-short: Unfavorable question → 5-second answer, move on
  Expand: Hits our strength → 30-second answer + bonus highlight
  Reverse: Challenge question → Acknowledge → Pivot to our solution
```

## Decision Mode Templates

| Decision Mode | English Description | Strategy Posture |
|--------------|--------------------|-----------------|
| Safety | Risk-averse decision maker; emphasizes "stability," "proven ROI," "risk control" | Lead with certainty, case studies, data, risk mitigation plans |
| Political | Multi-stakeholder dynamics; complex decision chain; internal competition | Design "win-win" for all stakeholders; avoid alienating any party |
| Aggressive | Ambitious decision maker; wants bold moves; brand transformation phase | Lead with big creative, disruptive propositions, high-reward vision |
| Procurement | Procurement-led; price-sensitive; standardized scoring | Lead with value-for-money, service commitments, execution guarantees |

## Checkpoint Format (English)

```
📌 Checkpoint [{step}/6]: {Agent Name} Complete

{Markdown summary}

---
Type "continue" to proceed, or share any adjustments.
```

## Progress Report (English)

```
✅ [2/6] Information Agent Complete — Client in transition phase; strategy gap identified in "emotional connection"
⏳ [3/6] Strategy Agent in progress...
```
