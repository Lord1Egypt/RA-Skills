# Imprint — Implementation Guide

## Quick Start

1. Create `imprint/` directory in your workspace
2. Copy `operator-model-schema.json` for reference
3. Add to your agent's session startup: "Load `imprint/operator-model.json` if it exists"
4. Add to your agent's session end: "Update `imprint/operator-model.json` with new observations"

That's it. The rest is the agent doing its job — watching, learning, adapting.

## Observation Extraction

After each meaningful interaction, the agent should ask itself:

### Decision Signals
- Did the operator choose between options? Which did they pick? How fast?
- Did they override a suggestion? What did they prefer instead?
- Did they accept without comment? (Implicit confirmation)

### Communication Signals
- How long was their message? (Word count relative to topic complexity)
- Did they use formal or casual language?
- Did they use humor? Sarcasm? Directness?
- Did they include pleasantries or skip to the point?

### Attention Signals
- Did they respond to this message at all?
- How quickly did they respond? (Fast = engaged, slow = low priority)
- Did they engage with the substance or just acknowledge?
- Did they ask follow-ups? (High engagement signal)

### Correction Signals (Highest Value)
- Did they edit your output? What did they change?
- Did they say "no, I meant..." — what was the gap?
- Did they rephrase your answer to someone else? How did it differ?
- Did they explicitly tell you to do something differently next time?

### Recording Format

Append to `imprint/observations/YYYY-MM-DD.md`:

```markdown
## Observation: [timestamp]
- **Category:** correction | decision | communication | attention | timing
- **Signal:** [what happened — derived behavioral signal only, never raw message content]
- **Trait update:** [which trait this affects]
- **Confidence delta:** [+/- how much this changes confidence]
```

**Important:** Never log raw message content in observations. Store only the derived behavioral signal. "Operator preferred shorter response" not the actual message. This is a hard rule.

## Model Updates

### When to Update

- After explicit corrections (immediate, high weight)
- After decisions between options (immediate, medium weight)
- End of session (batch update from accumulated signals)
- After periods of silence (absence is signal too)

### How to Update

For each new observation affecting trait `T`:

```
new_confidence = (old_confidence × old_count + signal_weight × signal_value) / (old_count + signal_weight)
```

Where:
- `old_count` = existing observation count (with decay applied)
- `signal_weight` = 5 for explicit corrections, 1 for implicit signals
- `signal_value` = 1 if signal confirms current trait value, 0 if contradicts

If a signal contradicts the current trait value AND has enough weight to shift confidence below 0.3, consider resetting the trait to a new value.

### Decay Application

Before each update, apply decay to existing observations:

```
effective_count = observations × e^(-decay_rate × days_since_last_update)
```

This means 30 days without reinforcement roughly halves the observation weight (at default λ=0.05).

## Anticipation Engine

### Decision Anticipation

When the operator faces a decision:
1. Check `decision_speed` trait
2. If "fast-intuitive" with high confidence: present the option you predict they'll choose as the default, others as alternatives
3. If "deliberate-analytical": present all options with equal weight and analysis
4. Track whether your prediction was right

### Communication Matching

Before generating any response:
1. Check `communication_style` and `detail_preference`
2. Match length, formality, and structure to the model
3. If `correction_pattern` indicates they remove hedging: don't hedge
4. If `correction_pattern` indicates they want more detail: give more detail

### Proactive Flagging

Based on `engagement_trigger` and `disengagement_trigger`:
- Proactively surface things matching engagement triggers
- Minimize or batch things matching disengagement triggers
- If `autonomy_preference` is high: do things silently, report only exceptions

### Context Pre-Loading

Based on `work_rhythm` and `active_hours`:
- During predicted active periods: have relevant context ready
- Predict what they'll work on based on recent patterns
- Pre-load relevant **workspace files** they're likely to need

**Scope constraint:** Pre-loading means reading files already in the workspace. It does not mean fetching from the network, calling APIs, or accessing data outside the workspace. The agent reads local files it already has access to — nothing more.

## Prediction Tracking

Every time the agent acts on a prediction from the model:

```json
{
  "timestamp": "2026-03-20T18:00:00Z",
  "prediction": "operator will prefer bullet format",
  "trait_used": "detail_preference",
  "confidence": 0.68,
  "outcome": "confirmed",
  "evidence": "operator engaged with bullet response without reformatting"
}
```

Track `predictions.accuracy` over time. If accuracy drops below 0.6, the model is stale — increase observation weight, decrease anticipation confidence, and consider a soft reset on low-confidence traits.

## Edge Cases

### Multiple Operators
If the agent serves multiple people (group chats, shared workspace):
- Maintain separate models per operator
- Use speaker identification to route observations
- In group settings, default to the most conservative model (least assumption)

### Contradictory Signals
Operator behaves differently in different contexts (casual in DMs, formal in groups):
- Track context tags on observations: `context: dm | group | work | casual`
- Allow traits to have context-specific values
- Don't average across contexts — keep them separate

### Operator Says "Stop"
If the operator asks the agent to stop a learned behavior:
- Immediate override. No argument.
- Record as high-weight correction
- Reset the relevant trait confidence to 0.0
- Don't silently resume the behavior later

### Model Inspection
The operator should always be able to:
- Read the full model (`imprint/operator-model.json`)
- Edit any trait or delete any observation
- Reset the entire model
- Ask "what do you think you know about me?" and get an honest answer

Transparency is non-negotiable. The model exists to serve the operator. It's their data.

## Privacy Principles

1. **Local only.** The model never leaves the workspace.
2. **Behavioral, not personal.** Track patterns, not secrets.
3. **Operator-owned.** They can read, edit, or delete it anytime.
4. **No content logging.** Store "operator preferred shorter response" not the actual messages.
5. **Transparent on request.** If asked, explain exactly what you've observed and why.
