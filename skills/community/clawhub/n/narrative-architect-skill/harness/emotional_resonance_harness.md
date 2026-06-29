# Emotional Resonance Harness

## Purpose

Check whether the output gives the target audience an emotional reason to care.

This harness is especially important for general public, media, customer-first-touch, and brand storytelling outputs.

Clarity is not enough. The audience must feel why the concept matters before being asked to understand it.

## Checkpoints

### 1. Felt Problem

Does the opening create a felt problem, not just define a concept?

Weak:

```text
Harness engineering is a set of checks before AI output is used.
```

Better:

```text
最可怕的 AI 错误，往往不是一眼就能看出来的错误。
```

### 2. Recognizable Scene

Is there a recognizable human scene or consequence?

The audience should be able to say "yes, I have experienced something like this" or "I can imagine this happening."

### 3. Tension Before Resolution

Does the text create tension before resolving it?

Do not explain the mechanism before the audience feels the problem. The sequence matters: problem felt → mechanism revealed → value understood.

### 4. Emotion from Real Stakes

Does the emotion come from real stakes?

Check that every emotional beat traces to a stake identified in the Value & Stakes analysis. If the emotional weight exceeds the real stakes, the narrative is overdramatized.

### 5. Ending Payoff

Does the ending create relief, urgency, conviction, or recognition?

The final emotion must differ from the initial emotion. If the audience ends where they started, the emotional arc is flat.

### 6. Melodrama Check

Does the text avoid melodrama?

Flag:

- "改变一切"
- "前所未有的"
- "彻底颠覆"
- "如果你不..."
- "灾难性的后果"

These signal forced emotion rather than earned feeling.

### 7. Controlling Idea Alignment

Does the emotional layer support the controlling idea?

The emotional arc should prove the controlling idea, not distract from it. If the strongest emotion in the text contradicts the controlling idea, the narrative is at war with itself.

## Failure Modes

Fail if:

- the text is clear but emotionally flat;
- the opening is a definition;
- the audience has no reason to care;
- the text explains before it makes the problem felt;
- emotion is exaggerated beyond evidence;
- metaphor replaces mechanism;
- the ending is a slogan rather than emotional resolution;
- the emotional temperature does not match the audience type;
- the emotion comes from the narrator's enthusiasm, not the material's stakes.

## Severity

```text
hard_fail:
 - no emotional reason to care (general audience, temperature ≥ 3)
 - emotion contradicts controlling idea
 - melodrama (inflated language beyond stakes)

soft_fail:
 - flat opening that could engage more
 - resolution too abrupt
 - recognizable scene missing for general audience
```

## Rewrite Rule

If emotional resonance is weak, rewrite using:

```text
felt risk
→ concrete scene
→ hidden problem
→ mechanism
→ emotional resolution
```

Example:

Weak:

```text
Harness engineering is a set of checks before AI output is used.
```

Better:

```text
最可怕的 AI 错误，往往不是一眼就能看出来的错误。
它听起来很对，读起来很顺，但关键地方悄悄改了意思。
等你发现的时候，它已经进了报告、邮件、或者给客户的文件里。
Harness engineering 的作用，就是在这一切发生之前，把输出拦住、查一遍、确认没问题再放行。
```

## Output Instruction

Do not expose the emotional arc analysis to the user unless:

- the user asks why the text feels flat;
- the user asks for audience-specific emotional shaping;
- the user is testing the skill;
- the task explicitly involves emotional or brand storytelling.

For normal output, use the harness internally and output only the improved draft.

## Final Rule

For general audiences, clarity is not enough.
The audience must feel why the concept matters before being asked to understand it.
