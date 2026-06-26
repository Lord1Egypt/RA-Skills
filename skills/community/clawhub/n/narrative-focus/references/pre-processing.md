# Pre-processing: Collection & Labeling SOP

## Applicable Scenarios

Doing deep research / knowledge collection on a technical domain, needing to ensure collected details won't cause narrative weight misalignment in subsequent writing.

## Core Principle

At collection time, you often don't yet know what's architectural vs. transport — because you haven't built a complete mental model yet. So pre-processing isn't about "judging right vs. wrong" — it's about **labeling collected items with role tags to give post-processing room to operate**.

## Workflow

### Step 1: Collect Details

Collect technical details normally. Don't skip any information that seems "unimportant."

### Step 2: Identify the Proposition Conveyed by Each Detail

Before applying the substitution test, determine **what proposition each detail is actually conveying in its source context**. The same technical term can carry different propositions.

For each collected detail, answer:

> **What is this detail actually asserting? What would a reader take away as the key insight?**

Do not skip this step — substituting the literal term instead of the proposition is the most common source of mislabeling.

### Step 3: Apply Substitution Test to Each Proposition

For each proposition identified in Step 2, answer:

> **If this proposition were replaced with an alternative, would the user's observable behavior change?**

Judgment rules:
- **Yes** → Label as `Architectural`
- **No, only the delivery method changes** → Label as `Transport`
- **Behavior unchanged, only configuration differs** → Label as `Configurable`

### Step 4: Record Labels and Rationale

For each technical detail, record:

```
- Detail: [name]
- Role Label: [Architectural / Transport / Configurable]
- Rationale: [what behavior would/wouldn't change if replaced]
- Expected Narrative Weight: [High / Low / Medium]
```

### Step 5: Flag Potential Misalignment Risks

If a detail meets any of these conditions, flag it as `Potential Misalignment Risk`:

1. **Familiarity-weighting risk**: The detail uses a common term (e.g., "event delegation", "virtual DOM") that easily leads readers to auto-complete processing logic using its classical meaning
2. **Length-induced risk**: The detail is extensively elaborated in source materials (independent chapter, lots of code examples) but is actually Transport/Configurable
3. **Implicit-completion risk**: The detail's name implies certain processing logic (e.g., "delegation" implies processing at the delegation point), but the actual processing logic is elsewhere

### Step 6: Output Collection

Output all collected technical details with their labels in a structured format for use in post-processing.

## Guidance for External Collection/Production

When requesting collection from external parties (e.g., AI agents, collaborators), append this requirement beyond "collect these technical details":

> **For each technical concept, in addition to explaining "what it is", answer: if it were replaced with an alternative implementation, would the user's observable behavior change? If yes, it's Architectural; if no, it's Transport.**

The key: this doesn't require collectors to make judgments before understanding the full picture — it gives them an operational rule.
