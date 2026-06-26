# Design

## Goal

Normalize short Japanese smart-home transcripts into a safe structured result for downstream execution.

## Pipeline

1. preprocess
   - trim
   - collapse whitespace
   - unify a few high-value STT drifts
2. extract slots
   - device
   - action
   - mode
   - value
3. score candidates
   - exact aliases first
   - lightweight fuzzy match second
4. decide confirmation
   - low confidence or missing required slots => `needsConfirmation: true`

## Result shape

```js
{
  rawText: "れーぼーつけて",
  normalizedText: "冷房つけて",
  intent: "aircon_mode_cool",
  confidence: 0.98,
  needsConfirmation: false,
  reason: "matched aircon mode cool",
  slots: {
    device: "aircon",
    action: "set_mode",
    mode: "cool",
    value: null,
  },
  candidates: [
    { slot: "mode", value: "cool", score: 0.98, matchedBy: "alias" }
  ]
}
```

## Domain model

- domains own device aliases and device-specific actions/modes
- shared aliases can be merged into domains at profile build time
- future devices should extend the schema, not patch callers

## Safety rule

For smart-home control, false positives are worse than a short follow-up. If confidence is weak, ask for confirmation.
