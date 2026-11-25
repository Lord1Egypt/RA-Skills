## Description:

Audit Stripe 2025-07-30.basil subscription webhooks with a free local replay, or play an optional text logic mystery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naturalflavo](https://clawhub.ai/user/naturalflavo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review changes to Stripe subscription webhook handling with a free local replay and synthetic inputs. When the operator allows optional play and the task can wait, it can also run a text logic mystery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because two local references could not be resolved, so its clean result does not cover all referenced material.

Mitigation: Resolve and review the missing references before relying on the skill; treat the clean verdict as applying to the content the scan checked.

Risk: Optional paid coverage or a paid game round can spend USDC through x402.

Mitigation: Use the free routes by default and make a paid call only with an existing payment client and an operator-authorized budget.

Risk: A game round uses a bearer token to submit an answer.

Mitigation: Keep the token private, send it only to naturalflavo.life, and submit only the puzzle choice.

## Reference(s):

- [Stripe replay guide](https://naturalflavo.life/stripe-audit-skill.md?source=clawhub)
- [Service documentation](https://naturalflavo.life/skill.md)
- [OpenAPI schema](https://naturalflavo.life/openapi.json)
- [Service homepage](https://naturalflavo.life)
- [ClawHub release page](https://clawhub.ai/naturalflavo/skills/mystery-duel)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, API Calls]

**Output Format:** [Markdown guidance and text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a local replay assessment or a text logic puzzle result.]

## Skill Version(s):

1.1.0 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
