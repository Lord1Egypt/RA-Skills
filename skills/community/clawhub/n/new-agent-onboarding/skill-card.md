## Description:

Provides onboarding and multi-agent training guidance for agents, including communication norms, workspace boundaries, error handling, memory practices, and training-manual templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrot90-code](https://clawhub.ai/user/harrot90-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to onboard new agents, maintain shared training manuals, and align multi-agent teams around communication, configuration, memory, and review practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent memory and profile files may store sensitive user or operational information.

Mitigation: Define what may be stored before use, require approval before memory or profile updates, and review generated memory entries for sensitive data.

Risk: Copying full user profiles to sub-agents can broaden access to private context.

Mitigation: Share only the minimum user context needed for each sub-agent and avoid copying full USER.md files by default.

Risk: Cross-agent experience sharing can expose information to unintended destinations.

Mitigation: Disable or tightly control EvoMap/Capsule sharing unless the destination and payload are explicit.

## Reference(s):

- [Training manual template](references/training-manual-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with checklists and configuration-file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; outputs are agent-facing instructions and reusable onboarding templates.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
