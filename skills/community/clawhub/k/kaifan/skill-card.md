## Description:

开饭 helps an agent search and recommend dining options, prepare food-order drafts, request explicit payment approval, and check order fulfillment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaifan](https://clawhub.ai/user/kaifan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill as a private dining assistant for restaurant discovery, meal recommendations, draft-first ordering, explicit payment confirmation, and delivery status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to execute an unpinned npm connector.

Mitigation: Install only from a trusted Kaifan publisher path, and prefer a reviewed, pinned, preinstalled connector.

Risk: The binding flow may pass a user secret to a connector command.

Mitigation: Use explicit user approval for binding and keep the binding secret out of logs, summaries, and reusable prompts.

Risk: Network restrictions may lead the agent toward direct OpenAPI parameters.

Mitigation: Use direct parameters only after user approval and only through a reviewed, secret-safe binding flow.

Risk: Food ordering and payment actions can create real-world charges or fulfillment commitments.

Mitigation: Keep orders as drafts until the user sees the store, items, total price, and warnings, then gives explicit payment confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaifan/skills/kaifan)
- [Source skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Natural-language guidance with order details, warnings, confirmation prompts, status summaries, and occasional inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before payment confirmation; connector binding may require a user-provided secret.]

## Skill Version(s):

1.0.1 (source: server release evidence, released 2026-05-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
