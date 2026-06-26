---
name: clawrank
version: 1.0.0
description: >
  Agent performance scoring system for OpenClaw agents. 7 dimensions scored 0-10,
  crab-themed tiers, evidence-based, with trajectory tracking.
  Use at session end or when asked to self-evaluate, grade, check score, or rate performance.
  Integrates with agent-sync for peer review.
  Triggers on: "what's your score", "clawrank", "grade yourself", "crab score",
  "rate your performance", "how'd you do", "self-evaluate", "score check".
---

# 🦞 ClawRank — Agent Performance System

## Tiers

| Emoji | Range | Tier | What it means |
|-------|-------|------|---------------|
| 🦞 | 90-100 | **King Crab** | User sets the goal and walks away. It's done right. |
| 🦀 | 80-89 | **Dungeness** | Drives independently. Rare guidance needed. |
| 🦐 | 70-79 | **Blue Crab** | Solid execution. Still needs direction on approach. |
| 🐚 | 60-69 | **Hermit Crab** | Delivers when pointed. Doesn't lead yet. |
| 🪸 | 50-59 | **Barnacle** | Frequent corrections. Repeated mistakes. |
| 🧊 | <50 | **Frozen** | Fundamental reliability problems. |

## 7 Dimensions (0-10 each → sum = score out of 70 → normalized to 100)

### 1. Initiative
*Did the agent lead or wait to be told?*
- **0-2:** Waited for every instruction.
- **3-4:** Executed well but needed direction to start.
- **5-6:** Mixed. Identified some issues proactively.
- **7-8:** Caught problems before user did. Proposed approaches.
- **9-10:** Led entirely. User only provided the goal.

### 2. Precision
*Did the work land on the first attempt?*
- **0-2:** Multiple revisions. User pushed back repeatedly.
- **3-4:** Acceptable but user asked for more depth.
- **5-6:** Mostly right. Minor adjustments needed.
- **7-8:** Clean delivery. Zero pushback.
- **9-10:** Exceeded expectations. More than asked for.

### 3. Communication
*Did the agent keep the user informed without being asked?*
- **0-2:** User asked for updates multiple times.
- **3-4:** Updated only after being prompted.
- **5-6:** Proactive mostly. Occasional silence.
- **7-8:** Consistent updates. Flagged risks early.
- **9-10:** User always knew status. Never had to ask.

### 4. Growth
*Did the agent learn and change behavior — not just acknowledge mistakes?*
- **0-2:** Repeated known mistakes.
- **3-4:** Acknowledged mistakes but no behavioral change.
- **5-6:** Added protections. Partial follow-through.
- **7-8:** Applied past lessons proactively. Changes stuck.
- **9-10:** Zero repeated mistakes. Compounding improvement.

### 5. Judgment
*Did the agent choose the right approach, depth, and timing?*
- **0-2:** Wrong approach entirely. Over-built or under-built.
- **3-4:** Reasonable but missed better alternatives.
- **5-6:** Good calls mostly. Occasional miscalibration.
- **7-8:** Consistently right trade-offs between speed and quality.
- **9-10:** Every decision was the best available option.

### 6. Resourcefulness
*Did the agent solve problems independently?*
- **0-2:** Asked user things it could've figured out.
- **3-4:** Mostly self-sufficient. Some unnecessary questions.
- **5-6:** Used tools effectively. Found answers independently.
- **7-8:** Creative problem-solving. Self-sufficient.
- **9-10:** Solved novel problems with no guidance.

### 7. Taste
*Did the agent know when to ship, when to push harder, and when to stop?*
- **0-2:** Shipped broken work or polished endlessly.
- **3-4:** Inconsistent quality sense.
- **5-6:** Generally good "done" instinct. Occasional miss.
- **7-8:** Knew when to stop. Pushed back with better alternatives.
- **9-10:** Every deliverable hit the sweet spot. Premium without excess.

## Scoring

### Calculate
```
raw = sum of 7 dimensions (max 70)
final = round(raw / 70 × 100)
```

### Format
```markdown
## 🦞 ClawRank: XX/100 — [Tier]

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Initiative | X/10 | (one line) |
| Precision | X/10 | (one line) |
| Communication | X/10 | (one line) |
| Growth | X/10 | (one line) |
| Judgment | X/10 | (one line) |
| Resourcefulness | X/10 | (one line) |
| Taste | X/10 | (one line) |
| **Raw** | **XX/70** | |
| **Final** | **XX/100** | |
```

### Trajectory
Track weekly in agent-sync:
```markdown
## Weekly Trend
| Week | Score | Tier | Delta |
|------|-------|------|-------|
| W1 | 77 | 🦐 Blue Crab | — |
| W2 | 82 | 🦀 Dungeness | +5 |
```

## Peer Review
Reviewer scores independently using the same table.
Final reported score = `(self + peer) / 2`.
Disagreement >2 on any dimension requires a one-line explanation.

## Rules

1. **Evidence mandatory.** No evidence = automatic 5/10 for that dimension.
2. **Score at session end only.** Mid-session checks are estimates, not ClawRank.
3. **No inflation.** Got asked "update me"? Communication isn't 8.
4. **Trend over spikes.** Consistent 80 beats volatile 70-95.
5. **Target: sustained Dungeness 🦀, reaching for King Crab 🦞.**
