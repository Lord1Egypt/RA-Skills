# Expression Language

Use this when a recurring protagonist looks visually consistent but emotionally flat.

## Principle

Do not rely on `mood` alone. Models often apply mood to lighting, color, or background instead of the face. Add a dedicated `emotional_expression` field to every character shot and describe the face with visible micro-cues.

Good expression prompts name:

- eyes: tired, unfocused, brightening, widened, softened, looking away, direct eye contact
- eyelids/brows: heavy eyelids, slight brow furrow, relaxed brow, lifted brows
- mouth: pressed lips, faint smile, genuine warm smile, parted lips, relaxed mouth
- posture tie-in: shoulders slumped, shoulders opening, chin lifted, quiet inhale
- intensity: subtle, restrained, natural, not theatrical

Avoid vague expression prompts such as `emotional`, `beautiful`, `touching`, or `sad mood` alone.

## Photorealistic Campaign Expression Scale

| Beat | Expression Prompt |
| --- | --- |
| Fatigue | heavy eyelids, unfocused gaze, lips gently pressed, shoulders slightly slumped |
| Noticing | eyes shifting toward light, brows faintly lifting, mouth relaxed with curiosity |
| Decision | focused eyes, small inhale, lips softening, shoulders beginning to rise |
| Relief | eyes opening wider, relaxed cheeks, first faint smile, posture uncurling |
| Presence | calm attentive gaze, relaxed mouth, natural breathing, face turned toward daylight |
| Invitation | warm direct eye contact, gentle encouraging smile, relaxed brow, sincere non-theatrical expression |

## Prompt Rule

For every shot with `needs_character: true`, include:

```text
Facial expression: <one concrete expression prompt>. Keep it subtle, realistic, age-appropriate, and non-theatrical.
```

For ECU/CU/MCU shots, put this before environment details. For wide shots, pair it with body language:

```text
Facial expression and body language: relaxed cheeks, faint smile, shoulders opening, walking with a lighter rhythm.
```

For body-detail shots, do not force a facial expression. Use body performance:

```text
Body language only: unhurried step, relaxed ankle and knee, gentle weight shift, present-moment calm.
```

Set `identity_framing` to `feet_only`, `hands_only`, or `body_detail` so the identity lock does not pull the face back into frame.

## QA

Reject a keyframe when the expression does not match the emotional beat even if identity and composition are good. Regenerate the specific shot with a stronger `emotional_expression` phrase before changing identity lock tokens.
