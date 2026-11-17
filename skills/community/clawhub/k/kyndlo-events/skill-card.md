## Description:

Kyndlo Events guides an agent through Kyndlo campaign-based event creation, venue research, duplicate checks, AI image generation, and event validation using the Kyndlo CLI workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pirumpi](https://clawhub.ai/user/pirumpi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators managing Kyndlo campaigns use this skill to create and validate event records from campaign tasks, including venue discovery, duplicate checks, recurring event setup, image attachment, and batch reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad live-system authority through Kyndlo CLI workflows, including admin, update, and delete examples.

Mitigation: Install only if you trust the Kyndlo CLI package, the Kyndlo dashboard administrators, and the token permissions; avoid admin, update, and delete commands unless those live changes are intended.

Risk: Remote dashboard rules influence event creation and may be under-scoped or change between batches.

Mitigation: Review dashboard rules before each batch and pause for human confirmation before creating events.

Risk: API tokens or other secrets could be exposed if pasted into chat or logs.

Mitigation: Use least-privilege tokens and avoid pasting secrets into chat, command transcripts, or logs.

## Reference(s):

- [Kyndlo Events ClawHub release](https://clawhub.ai/pirumpi/skills/kyndlo-events)
- [Kyndlo CLI homepage](https://github.com/kyndlo/gokyn-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with shell command blocks and JSON-oriented CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KYNDLO_API_TOKEN, node, and gokyn; venue discovery uses goplaces and GOOGLE_PLACES_API_KEY when creating events.]

## Skill Version(s):

3.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
