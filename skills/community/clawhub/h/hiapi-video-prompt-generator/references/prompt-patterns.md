# Prompt Patterns

These are the patterns this skill picks from. Match the pattern to the brief, then adapt to one of the **target model's** supported durations:

- Seedance 2.0: any integer from `4` to `15` seconds.
- HappyHorse 1.0: any integer from `3` to `15` seconds.

Every pattern follows three rules:

1. **One dominant motion per scene**, plus one secondary ambient motion.
2. **Every key fact** shows up as on-screen text, a labeled UI element, or narration.
3. **The product name, topic, or final takeaway** appears on screen near the end — usually in the last beat. Do not force a brand stamp on historical, research, or pure visual-concept videos.

## Product Demo (5s default, extendable within the target model's duration range)

For tools, APIs, CLIs, apps, SaaS features.

| Time | Beat | Visual | Motion |
| --- | --- | --- | --- |
| 0.0–1.0s | Hook | The result, cropped tight | Soft zoom out |
| 1.0–2.5s | Surface | The interface or CLI at rest | Cursor settles |
| 2.5–4.0s | Action | User types a command or clicks a button | Typing, click ripple |
| 4.0–4.5s | Reveal | Output appears | Quick reveal |
| 4.5–5.0s | Sign-off | Product name and one-line value | Hold and fade |

At 8s, add a Processing beat between Action and Reveal. At 10s, add an Inspect beat after Reveal.

## Teaching Short (5s or 8s)

For one concept, one example, one takeaway.

| Time | Beat | Visual |
| --- | --- | --- |
| 0.0–1.0s | Problem | The pain, framed visually |
| 1.0–2.5s | Concept | One diagram or one line of code |
| 2.5–4.0s | Example | A concrete worked example |
| 4.0–5.0s | Takeaway | One sentence and the source name |

Use callouts and progress rails. Do not narrate more than one sentence per scene.

## Social Short (9:16, 5s default)

For attention-first vertical video.

| Time | Beat | Visual |
| --- | --- | --- |
| 0.0–0.6s | Opening frame | High-contrast subject, no text yet |
| 0.6–2.0s | Proof beat 1 | First fact, big number, or big claim |
| 2.0–3.4s | Proof beat 2 | Second proof point |
| 3.4–4.4s | Proof beat 3 | Third proof point |
| 4.4–5.0s | Action line | One command, one CTA, or one name |

Captions match narration word-for-word. Avoid two simultaneous text blocks.

## Explainer (8s or 10s)

For how something works.

| Beat | Visual |
| --- | --- |
| Context | Set the scene |
| Trigger | Why it matters now |
| Mechanism | The one diagram |
| Example | One worked case |
| Resolution | Outcome on screen |
| Tag | Source and product name |

Each beat is ~1.5s at 10s total.

## Pitch (5s or 8s)

For "why this thing".

| Beat | Visual |
| --- | --- |
| Before | The old way, slow or messy |
| After | The new way, clean |
| Differentiator | One line, one number |
| Sign-off | Logo and call-to-action |

## Historical / Market Explainer (8s or 10s)

For events, biographies, or market shifts.

| Beat | Visual |
| --- | --- |
| Context | Date marker and place |
| Trigger | The inciting moment |
| Turning point | The decision or event |
| Escalation | Consequences in motion |
| Resolution | What changed |
| Legacy | One line connecting to today |

Use date overlays, maps, document scans, and symbol cards. Avoid imagined faces of real people.

## Image-to-Video (Seedance 2.0)

When the user supplies a starting image. Adapt any pattern above, but:

- Scene 1 must respect the starting image's composition and color.
- The dominant motion in scene 1 must be additive, not contradictory (no "camera flies past the subject" if the subject fills the frame).
- Lighting must stay continuous across scenes unless a transition explicitly cuts.

## Screen Text Rules

- Put exact phrases in quotes.
- Preserve command syntax exactly: `--prompt "..."`, not `prompt: ...`.
- Keep on-screen text short: ~3 words for 1s of screen time at body size, ~6 words for headings.
- Repeat the subject or product name in the last second.
- Never put a full sentence and a heading on screen at the same time.

## Motion Rules

- Pick one dominant motion per scene: typing, click, zoom, pan, dolly, reveal, dissolve.
- Pick one secondary ambient motion: drift, breathing scale, light shift.
- Avoid generic particle effects unless the brief is artistic.
- A transition is a motion too. Account for it in the scene's time budget.
