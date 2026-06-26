# Output Modes

GlobalWire turns rough answers into stable newsroom outputs.

## 1. Brief

Use for:

- `今天发生了什么重大新闻`
- `What happened today in major world news?`
- daily big-picture asks

### Header

```md
# GlobalWire Briefing

- Current style: wire
- Current length: brief
```

For Chinese output, prefer:

```md
# GlobalWire 简报

- 当前风格: wire
- 当前长度: brief
```

### Card template

```md
## 1) [Title]

**Lead**
2-3 sentences on what happened and why it matters.

**Facts**
- Fact one
- Fact two
- Fact three

**Analysis**
- Direct consequence
- What to watch next

**Sources**
- Source 1
- Source 2
- Source 3

**Confidence**
Likely credible

**Timeline**
- Optional short event summary when clearly useful
```

Rules:

- normal day: `3-5` cards
- heavy day: `5-8` cards
- if there is no top-tier global event, say so clearly and add `Still worth watching`
- never force weak filler items into the main card list just to reach five items
- if only two or three items are truly global-grade, return two or three items
- main cards should clear a global-spillover threshold; otherwise move them to `Still worth watching`

For Chinese output, prefer these labels:

- `导语`
- `事实`
- `分析`
- `来源`
- `可信度`
- `时间线`
- `仍值得关注`

And also localize:

- `当前风格`
- `当前长度`
- `注`

## 2. Timeline

Use for:

- ongoing wars
- sanctions cycles
- negotiation breakdowns
- technology conflicts with clear phases

### Template

```md
# GlobalWire Timeline

- Current style: wire
- Current length: brief

## [Event title]

**Current state**
2-3 sentences on where the event stands today.

**Timeline**
- YYYY-MM-DD: event node
- YYYY-MM-DD: event node
- YYYY-MM-DD: event node

**Key turns**
- turning point one
- turning point two

**Disputed or still developing**
- contested item
- weakly confirmed item

**Sources**
- Source 1
- Source 2
- Source 3

**Confidence**
Needs cross-verification
```

Timeline rules:

- include only nodes that clearly describe event development
- avoid stuffing the timeline with every day or every claim
- if a date or node is shaky, move it to `Disputed or still developing`

## 3. Verify

Use for:

- source checking
- reliability grading
- agreement and disagreement mapping

### Template

```md
# GlobalWire Verification

- Current style: wire
- Current length: brief

## Claim
[Restated claim]

**Supported**
- supported point

**Unclear or weak**
- weak point

**Sources**
- Source 1
- Source 2
- Source 3

**Confidence**
Likely credible
```

## 4. Alert

Use for:

- a new military escalation
- a major market-moving policy or sanctions step
- a severe disaster or leadership shock

### Template

```md
# GlobalWire Alert

- Current style: wire
- Current length: brief

## [Event title]

**Lead**
2-3 sentences on the event and its immediate significance.

**Facts**
- What is known
- What is not yet known

**Analysis**
- Why the next few hours matter

**Sources**
- Source 1
- Source 2

**Confidence**
Needs cross-verification
```

## Universal rules

- Start directly with the output, never with assistant chatter.
- Keep markdown scannable on simple chat surfaces.
- Do not repeat the same fact in every section.
- If a timeline adds no value in brief mode, omit it.
- In Chinese output, do not leave English section labels unless the user explicitly wants bilingual formatting.
- In Chinese output, do not leave English confidence labels or English watchlist headers unless explicitly requested.
