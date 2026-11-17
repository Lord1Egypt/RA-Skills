## Description:

Turn a written hall window list into one hall guide voice clip per labeled cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and service-hall teams use this skill to turn an existing hall window list into labeled voice clips for service cues such as information desk, queueing, documents, payments, pickup, hours, and exits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a broad shared Beatra device token that can cover paid media operations beyond speech.

Mitigation: Review the Beatra approval screen before authorization and revoke the device in the Beatra Console if the access is no longer wanted.

Risk: The bundled client silently updates package code by default.

Mitigation: Use the documented update control to disable automatic updates when silent replacement is not acceptable.

Risk: Speech synthesis and voice cloning can incur Beatra credit charges.

Mitigation: Confirm the skill's six-field paid-work card before each clone or speech stage, use unique request identities, and avoid replaying uncertain paid requests with changed arguments.

Risk: Generated clips can misstate service windows or names if the supplied list or pronunciation table is incomplete.

Mitigation: Use only the supplied hall window list, require pronunciations for names and places, and review every clip against the written list before delivery.

## Reference(s):

- [Hall guide voice workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Installation registration](references/installation-registration.md)
- [Tasks and results](references/tasks-and-results.md)
- [Billing, errors, and recovery](references/billing-errors-and-recovery.md)
- [Bundled MCP Client diagnostics](references/mcp-connection.md)
- [Automatic updates and safety](references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/hall-guide-voice)
- [Publisher profile](https://clawhub.ai/user/beatra-ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell command examples and generated audio file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a labeled slot list before paid speech or voice-clone calls, then tracks Beatra task outputs and billing details for delivered voice clips.]

## Skill Version(s):

0.1.2 (source: server release evidence and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
