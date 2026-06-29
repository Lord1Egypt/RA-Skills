# Narrative Entropy Mapper

## Purpose

Narrative Entropy Mapper determines how much predictability, surprise, and cognitive load the output should contain.

It runs after Affective Arc Mapper and before Audience Entry Point Selector.

## Required Output

```yaml
narrative_entropy:
  audience_entropy_tolerance:
  current_material_entropy:
  low_entropy_ground:
  high_entropy_turn:
  surprise_point:
  cognitive_load_risk:
  pacing_plan:
  compression_need:
  resolution_point:
```

## Field Definitions

### audience_entropy_tolerance

How much surprise or conceptual novelty can the audience tolerate?

Options:

```text
low
medium
high
```

Examples:

```text
child audience: low
general public: low to medium
business audience: medium
technical team: medium to high
expert audience: high
investor audience: medium to high
```

### current_material_entropy

Is the source material already dense or unfamiliar?

Options:

```text
low: familiar, simple
medium: some specialized terms
high: abstract, technical, multi-layered
```

If source entropy is high, the renderer should first reduce cognitive load before adding surprise.

### low_entropy_ground

The familiar base where the audience can stand.

Examples:

```text
开会时各部门数字对不上。
AI 写得很顺，但不一定可靠。
出海前要搞清楚法规、医院、渠道和支付。
小朋友玩闯关游戏前需要地图。
```

### high_entropy_turn

The insight that breaks expectation.

Examples:

```text
问题不在数据缺失，而在数据之间断了线。
最危险的 AI 错误不是写得差，而是写得太像真的。
真正压缩的不是时间，而是盲撞次数。
不是你缺信息，而是你缺一张能让信息互相看见的图。
```

### surprise_point

Where should the surprise appear?

Options:

```text
opening
after scene
middle reversal
ending line
```

General rule:

```text
Do not put maximum surprise in the first sentence unless the audience already has enough context.
```

### cognitive_load_risk

What may overload the audience?

Examples:

```text
too many acronyms
too many abstractions
too many entities
too many claims
too many metaphors
too many directions
```

### pacing_plan

The rhythm of the output.

Possible structures:

```text
low → medium → high → low
scene → turn → explain → resolve
problem → surprise → mechanism → consequence
familiar → strange → clear → memorable
```

### compression_need

Should the output compress complexity?

Options:

```text
low
medium
high
```

For short video, one-on-one message, child audience, or first-touch communication, compression_need is high.

### resolution_point

Where the audience lands emotionally or cognitively.

Examples:

```text
now I understand why this matters
now I see the hidden risk
now I know what changed
now I want to ask more
now I see why this is relevant to me
```

## Entropy Balance Rules

### Rule 1: Do not start with high abstraction

Bad:

```text
MSIA is a multi-agent world-model simulation architecture.
```

Better:

```text
A company trying to enter a new medical market often fails before it knows which mistake it made.
```

### Rule 2: One strong turn is better than many small surprises

Avoid stacking:

```text
world model
ontology
multi-agent
payment curve
KOL network
resource optimization
```

Choose one turn and build around it.

### Rule 3: Lower entropy before raising entropy

If the material is technical, first give the audience ground.

### Rule 4: Surprise must reveal structure

A surprise is not a punchline. It should reveal a deeper pattern.

Bad:

```text
This changes everything.
```

Better:

```text
The real change is not that the answer comes faster, but that the wrong path becomes visible earlier.
```

### Rule 5: Entropy must serve the controlling idea

Do not add surprise for entertainment alone.

## Final Rule

the skill should make the audience feel:

```text
I understand this.
But I also did not see it this way before.
```
