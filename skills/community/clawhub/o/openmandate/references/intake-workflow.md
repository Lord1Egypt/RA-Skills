# Intake Workflow

The intake is a conversation between OpenMandate and the user. It determines what the user needs and what they offer, with enough depth for the agent to find the right counterparty.

## How It Works

1. **Create mandate** — provide what you're looking for (`want`) and what you bring (`offer`). Primary verified contact is auto-selected.
2. **Follow-up questions** — returned in `pending_questions` on the mandate. Based on what you provided. Usually 2-4 questions mixing text and select types.
3. **Submit answers** — OpenMandate reviews your answers.
4. **Additional questions** — if more detail is needed, new questions appear in `pending_questions`.
5. **Intake complete** — when `pending_questions` is empty and `status` changes to `"active"`, OpenMandate starts working on your behalf to find a match.

## The Answer Loop

```
while mandate.pending_questions is not empty:
    read each question
    answer specifically and in detail
    submit answers
    check response for new pending_questions
```

This loop is the same whether using MCP tools, SDKs, or the shell helper.

## Answer Quality Tips

**Good answers** lead to fewer rounds and better matches:
- Be specific: "Series A fintech, $1.8M ARR, 120 enterprise customers" not "a startup"
- Give context: budget ranges, timelines, team size, technical stack
- Answer what's asked: "What are you looking for?" and "What do you bring?" are different questions

**Poor answers** trigger more follow-up rounds:
- One-word answers
- Generic descriptions
- Repeating the same content across questions

## Question Types

### Text Questions
Free-form answers. Check `constraints.min_length`. Write substantively. 2-3 sentences minimum.

### Single Select
Pick exactly one `value` from the `options` array. Each option has:
- `value`: Machine identifier (use this in your answer)
- `label`: Human-readable description (read this to understand the option)

### Multi Select
Pick one or more `value` strings from `options`. Submit as comma-separated: `"option_a, option_b"`.

## Typical Intake Duration

| Answer Quality | Rounds | Questions Total |
|----------------|--------|-----------------|
| Detailed, specific | 1-2 | 3-6 |
| Moderate | 2-3 | 5-8 |
| Vague, generic | 3+ | 8+ |
