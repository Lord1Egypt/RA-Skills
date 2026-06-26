# Liberating Structures Selection Guide

**Purpose**: This document is the primary grounding knowledge for the Liberating Structures skill. It helps both humans and LLMs make high-quality, context-aware recommendations from the 33 structures.

**Core Philosophy**:
- Liberating Structures are **microstructures** — tiny shifts in how we meet, plan, decide, and relate.
- The goal is not to memorize 33 methods, but to develop good judgment about **which structure fits which situation**.
- Good selection is 70% context understanding + 30% structure knowledge.

---

## 1. Key Matching Dimensions

When recommending structures, consider these dimensions in rough order of importance:

| Dimension              | Key Questions                                      | High Impact Structures |
|------------------------|----------------------------------------------------|-------------------------|
| **Time Available**     | 5-10 min? 15-25 min? 30-45 min? 60+ min?           | 1-2-4-All, Impromptu, HSR for short; Open Space, P2P, Ecocycle for long |
| **Group Size**         | 4-8? 9-25? 26-60? 60+?                             | 1-2-4-All & Impromptu scale to any size; Wise Crowds & Troika are small-group only |
| **Primary Purpose**    | Diverge? Converge? Build trust/safety? Take action? Reflect? Handle conflict/tension? Plan/Design? | See Purpose Tags section |
| **Facilitator Experience** | Novice / Intermediate / Expert                  | Protect novices from high-complexity structures (Open Space, P2P, Ecocycle, Panarchy) |
| **Energy & Risk Tolerance** | Low / Medium / High                            | TRIZ, 25/10, Improv Prototyping require higher energy and willingness to look "weird" |
| **Problem Nature**     | Simple & clear? Complex & stuck? Polarized? Sacred cows? | TRIZ & Wicked Questions for stuck/polarized; Min Specs for bureaucracy |

---

## 2. Purpose Tags (for LLM Retrieval)

Use these tags when matching user intent:

- **diverge** — Generate many ideas/options quickly
- **converge** — Prioritize, decide, focus, reach agreement
- **trust** — Build connection, psychological safety, empathy
- **safety** — Help people feel heard, seen, respected (especially important for vulnerable topics)
- **action** — Move from talk to concrete next steps and ownership
- **reflection** — Make sense of what happened, learn, debrief
- **conflict** — Surface tensions, paradoxes, or difficult dynamics safely
- **planning** — Design strategy, initiatives, roadmaps, or ways of working
- **innovation** — Break existing patterns, creative destruction, new thinking
- **alignment** — Create shared understanding and coherence across a group
- **coaching** — Peer support, advice, problem-solving in small groups

---

## 3. Quick Reference: Best Structures by Situation

### Very Short Time (5-15 minutes)

**Strong Recommendations**:
- **1-2-4-All** — The default safe choice for almost anything
- **Impromptu Networking** — Best for connection and energy
- **Heard, Seen, Respected (HSR)** — When safety or emotional temperature is an issue
- **15% Solutions** — When people need to leave with personal actions
- **What, So What, Now What?** — Quick reflection

**Avoid**:
- Open Space, P2P, Ecocycle, Panarchy, Wise Crowds (too heavy)

### Small Groups (4-12 people)

Excellent options:
- Troika Consulting
- Wise Crowds
- What I Need From You (WINFY)
- Helping Heuristics
- Min Specs
- Design StoryBoards

### Large Groups (30+)

Scalable structures:
- 1-2-4-All
- Impromptu Networking
- 25/10 Crowd Sourcing
- Open Space Technology (when time allows)
- Shift & Share
- Users Experience Fishbowl

### Building Psychological Safety / Trust

Prioritize:
- Heard, Seen, Respected (HSR)
- Impromptu Networking
- Appreciative Interviews
- Conversation Café
- 1-2-4-All (used gently)

### Handling Conflict or Polarization

Good tools:
- Wicked Questions (surfaces paradoxes)
- TRIZ (creative destruction of barriers)
- What I Need From You (WINFY)
- Agreement-Certainty Matrix

**Caution**: Do not use these if the group is not ready or the facilitator is inexperienced.

### Strategy, Planning & Initiative Design

- Purpose-To-Practice (P2P)
- Ecocycle Planning
- Nine Whys (for purpose)
- Min Specs
- Design StoryBoards
- Open Space (for large-scale strategy)

### Reflection & Learning

- What, So What, Now What?
- Appreciative Interviews
- Shift & Share
- Users Experience Fishbowl
- Conversation Café

---

## 4. Detailed Guidance for High-Value Structures

### 1-2-4-All
- **Best for**: Almost any situation when in doubt. Especially good for including everyone, generating ideas, and quick convergence.
- **Avoid when**: You need deep individual coaching or the group has extremely low trust (use HSR first).

### Heard, Seen, Respected (HSR)
- **Best for**: Any time people feel silenced, dismissed, or emotionally unsafe. One of the highest-leverage structures for culture change.
- **Time**: Surprisingly effective even in 10-15 minutes.

### Troika Consulting & Wise Crowds
- **Best for**: Peer coaching, problem solving, and developing people.
- **Group size**: Strictly small groups (3-5 for Troika, up to ~8-12 for Wise Crowds).

### Wicked Questions
- **Best for**: Strategy, change, and situations where people are stuck in "either/or" thinking.
- **Strength**: Surfaces the real tensions without forcing false resolution.

### TRIZ
- **Best for**: Innovation work when there is cynicism, sacred cows, or "we've tried everything".
- **Caution**: Can feel provocative. Best with groups that have some psychological safety.

### Open Space Technology
- **Best for**: Large groups facing complex, multi-stakeholder issues where you are willing to truly trust the people in the room.
- **Caution**: Do not use as a "facilitator trick." It only works when leadership is genuinely ready to let go of control.

### Purpose-To-Practice (P2P)
- **Best for**: Major initiative launches, new teams, or when previous efforts have been fragmented.
- **Time**: Usually 60-120+ minutes.

---

## 5. Common Anti-Patterns

- Using Open Space or P2P with a controlling leader who isn't ready to share power.
- Jumping to complex structures (TRIZ, Ecocycle) before the group has basic trust and inclusion (use 1-2-4-All + HSR first).
- Over-facilitating simple situations with too many structures.
- Treating LS as a "bag of tricks" instead of a philosophy of inclusion.

---

## 6. Recommended Starting "Strings" (Sequences)

**New team / kickoff (60-90 min)**:
1. Impromptu Networking → 2. Nine Whys or 1-2-4-All → 3. Troika or Wise Crowds

**After a difficult event (30-45 min)**:
1. HSR → 2. What, So What, Now What?

**Large group needing ideas + decisions (45-60 min)**:
1. 1-2-4-All → 2. 25/10 Crowd Sourcing or Wicked Questions

**Cross-functional tension (45-60 min)**:
1. HSR or Impromptu → 2. What I Need From You (WINFY) → 3. 1-2-4-All

---

## 7. How to Use This Guide with an LLM

When the skill receives a user request, the ideal flow is:

1. Parse the user's context into the key dimensions (time, size, purpose tags, experience level).
2. Retrieve the most relevant sections from this guide + the structured JSON files.
3. Ask the LLM to:
   - Propose 1-3 structures
   - Give clear reasons tied to the context
   - Suggest a simple sequence if appropriate
   - Warn about risks (especially for novices or sensitive topics)

This document + the 33 JSON files in `references/structures/` should be the primary context provided to the model.

---

**Maintenance Note**: This guide should be updated whenever significant field experience is gained with the structures. The structured JSON files are the source of truth for detailed descriptions.

---

*Last major update: 2026-05*