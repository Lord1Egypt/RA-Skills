## Description:

Helps an agent create, inspect, and edit Microsoft PowerPoint and PPTX presentations with Chinese-language interaction support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, business users, and automation teams use this skill to guide creation, inspection, and editing of PowerPoint presentations and PPTX files. It is best suited to structured presentation automation tasks rather than complex decisions that require human judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose shell commands or file writes while working with presentation files.

Mitigation: Give the agent specific file paths and review proposed shell commands or writes before allowing changes.

Risk: Presentation content may contain sensitive business information.

Mitigation: Avoid sharing unnecessary sensitive content and review generated or edited slides before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pptx-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with optional JSON status summaries, inline code or shell commands, and generated or edited PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include execution logs, result metadata, and file paths for generated or modified presentation assets.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
