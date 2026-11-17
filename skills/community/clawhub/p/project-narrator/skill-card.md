## Description:

Generate, audit, and maintain a PROJECT-NARRATIVE.md file that captures a project's architecture, decisions, infrastructure, and state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tcd004](https://clawhub.ai/user/tcd004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create and maintain a living project narrative that documents architecture, infrastructure, configuration, security model, design decisions, and operational drift. It supports generation, audit, update, and read-only health-report workflows for project documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated narratives centralize architecture, infrastructure, configuration, credential-location references, and other operational metadata.

Mitigation: Review PROJECT-NARRATIVE.md before committing or sharing it, keep real secrets out of the narrative, and use the skill only in repositories where this inventory is acceptable.

Risk: The optional URL checker can contact arbitrary URLs found in a narrative file.

Mitigation: Avoid --check-urls on untrusted narratives and in networks where localhost, intranet, or cloud metadata endpoints are reachable.

## Reference(s):

- [Project Narrator ClawHub listing](https://clawhub.ai/tcd004/skills/project-narrator)
- [Narrative template](references/narrative-template.md)
- [Narrative examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown narrative files, text audit findings, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write PROJECT-NARRATIVE.md and narrative archives; optional URL checking can make outbound HTTP HEAD requests.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
