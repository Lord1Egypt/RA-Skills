---
name: objective-evaluator
description: 客观原则评价技能 - Evaluate products, ideas, or designs using objective principles from three design classics. Based on Tony Fadell's Build (painkiller vs vitamin), Don Norman's Design of Everyday Things (three levels of design), and Dieter Rams' Ten Principles (red flags). Use when asked to evaluate, review, critique, judge, or assess any product, service, feature, tool, or design concept objectively. Triggers on phrases like "evaluate this", "what do you think of", "review", "judge", "audit", "评价", "怎么样", or when assessing product-market fit, usability, or design quality.
---

# Objective Evaluator - 客观原则评价技能

基于三本经典设计著作的客观评价框架：
- **Tony Fadell《Build》** - 止痛药 vs 维生素
- **Don Norman《设计心理学》** - 设计的三个层次
- **Dieter Rams《设计十诫》** - 红旗警告

Evaluate any product, idea, or design through three complementary lenses:

Evaluate any product, idea, or design through three complementary lenses:

## 🔧 Tool (Painkiller vs Vitamin)

Based on **Tony Fadell - Build**

Ask:
- Does it solve a real physical/information pain point?
- If it breaks tomorrow, does the workflow stop?
- Is it a painkiller (essential) or vitamin (nice-to-have)?

**Scoring:**
- ✅ **Tool** - Solves real pain, workflow depends on it
- ⚠️ **Edge Tool** - Painkiller for some, vitamin for others  
- ❌ **Not a Tool** - No real pain point addressed

## 🎨 Toy (Three Levels of Design)

Based on **Don Norman - Design of Everyday Things**

Evaluate across three levels:

| Level | Question | What to check |
|-------|----------|---------------|
| **Visceral** | Does it bring immediate pleasure/aesthetic satisfaction? | First impression, visual appeal, emotional response |
| **Behavioral** | Is the affordance natural? Does it work as expected? | Usability, feedback, control, error prevention |
| **Reflective** | Does it create long-term attachment/identity? | Personal meaning, self-image, long-term satisfaction |

**Scoring:**
- ✅ **Strong Toy** - Delivers on 2+ levels effectively
- ⚠️ **Weak Toy** - Delivers on 1 level only
- ❌ **Not a Toy** - No emotional or experiential value

## 🚩 Trash (Red Flags)

Based on **Dieter Rams - Ten Principles of Good Design**

Check for these deal-breakers:

| Red Flag | Description | Example |
|----------|-------------|---------|
| **Physics Violation** | Violates physical laws or logical impossibility | Perpetual motion, impossible chemistry |
| **Marketing Fiction** | Creates pseudo-demand through manipulation | "You need this" when you don't |
| **Dishonest Design** | Deceives users about function or origin | Fake buttons, hidden costs, dark patterns |
| **Planned Obsolescence** | Designed to fail unnecessarily | Non-replaceable batteries, software locks |

**Scoring:**
- 🚩 **Trash** - Any red flag present
- ⚠️ **Yellow Flag** - Borderline marketing stretch
- ✅ **Clean** - No red flags

## 📊 Final Verdict

Synthesize into clear classification:

```
┌─────────────────────────────────────────┐
│  TOOL + Strong Toy + Clean  →  KEEP ✅  │
│  TOY (only) + Clean         →  MAYBE ⚠️ │
│  Any + Trash flag           →  REJECT 🚮 │
└─────────────────────────────────────────┘
```

## 🎯 Usage Pattern

When evaluating something:

1. **Run the three audits** independently
2. **Note tensions** (e.g., strong Tool but weak Toy = industrial equipment)
3. **Identify user segments** (Tool for pros, Toy for consumers)
4. **Deliver verdict** with nuance about who it's for

## 💡 Key Insights to Surface

- **Business model cleverness** - How do they make money vs what they sell?
- **Identity play** - Are they selling functionality or self-image?
- **Marketing vs Reality** - Where does the story diverge from truth?
- **Segment dependency** - Different answers for different users

## Example Output Format

```markdown
## [Product Name] - T3 Audit

### 🔧 Tool Assessment
| Question | Answer |
|----------|--------|
| Real pain point? | ✅ Yes - ... |
| Workflow critical? | ⚠️ Partial - ... |

**Verdict:** Edge Tool (pros yes, casual users no)

### 🎨 Toy Assessment  
| Level | Score | Notes |
|-------|-------|-------|
| Visceral | ✅ | Beautiful industrial design |
| Behavioral | ⚠️ | Learning curve exists |
| Reflective | ✅ | "Pro user" identity |

**Verdict:** Strong Toy

### 🚩 Trash Check
- Physics violation? ❌ No
- Marketing fiction? ⚠️ Yellow flag - ...
- Dishonest design? ❌ No

### 📊 Final Verdict
**Segment-dependent:** TOOL for professionals, TOY for enthusiasts
```
