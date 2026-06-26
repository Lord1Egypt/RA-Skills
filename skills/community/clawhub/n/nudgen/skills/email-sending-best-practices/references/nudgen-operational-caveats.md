# Nudgen Operational Caveats

## Sending And Tracking Behavior

- Nudgen sending is Postmark-backed.
- Open, click, and unsubscribe flows depend on tracking endpoints and campaign link instrumentation.
- Preview and tracked-preview behavior should be validated before large sends.

## Contact State And Suppression

- Contact status drives send eligibility (`active`, `unsubscribed`, `bounced`).
- Campaign targeting should respect suppression and unsubscribe state.
- Do not assume imported contacts are immediately safe for full-volume sends.

## Team And Brand Boundaries

- Most operational behavior is team-scoped.
- Sender identity and tone are influenced by brand configuration.
- Switching active team changes command/API result context.

## Campaign Guardrails

- Campaign stop rules and scheduling settings materially affect risk and recipient experience.
- Validate stop conditions before enabling sends at scale.
- For incomplete or placeholder CLI flows, use API or dashboard workflows where needed.

## Practical Guidance

- If recommendations depend on Nudgen runtime behavior, call that out explicitly.
- If the user needs exact endpoint payloads after policy guidance, route to the `api` skill.
