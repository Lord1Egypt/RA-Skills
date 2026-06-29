# Audience Entry Point Selector

## Purpose

Choose the first door into the explanation.

A correct concept can still fail if it enters through the wrong door.

## Entry Point Types

### Risk-first

Use for:
- zero-AI-background audience
- executive audience
- customer audience
- high-stakes domains

Pattern:
"AI / a system / a process can appear correct while hiding mistakes."

Example:
"AI can give a fluent answer, but it may also make mistakes that are hard to notice."

### Pain-first

Use for:
- customers
- operators
- business users

Pattern:
"People currently lose time, money, or trust because..."

Example:
"Teams often discover AI mistakes only after the output has already entered real work."

### Mechanism-first

Use for:
- technical teams
- product teams
- architects

Pattern:
"This adds a checkable control layer between generation and delivery."

### Contrast-first

Use for:
- investor
- strategic narrative
- thought leadership

Pattern:
"The important shift is not from worse AI to better AI, but from uncontrolled output to controlled delivery."

### Scene-first

Use for:
- public communication
- speeches
- articles

Pattern:
"Imagine an AI writes a medical note, a legal memo, or a financial report..."

## Selection Rules

```text
If audience_label = zero_ai_background:
 use risk-first or scene-first.
 do not use mechanism-first.

If audience_label = technical_team:
 use mechanism-first.
 analogy optional.

If audience_label = investor_nontechnical:
 use contrast-first or business-consequence-first.

If audience_label = customer_first_touch:
 use pain-first.

If output length < 500 Chinese characters:
 use only one entry point.
```

## Failure Modes

Bad:
"Harness engineering is not prompt engineering."

Why bad:
It starts from insider contrast.

Better:
"AI can sound confident even when it is wrong."

Why better:
It starts from a risk ordinary people understand.
