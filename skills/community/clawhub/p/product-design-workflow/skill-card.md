## Description:

Guides an agent through a daily product design workflow that creates three consumer finance product ideas, turns them into PRDs, builds HTML prototypes, uploads demos, and reports progress step by step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoovaycn](https://clawhub.ai/user/hoovaycn)

### License/Terms of Use:

MIT-0

## Use Case:

External product teams and developers use this skill to repeatedly generate finance-oriented consumer product ideas, PRD documents, HTML demos, and status reports. It is intended for rapid product brainstorming, prototype creation, demo publishing, and daily product proposal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password-based SSH upload commands can expose server credentials when passwords are passed on the command line.

Mitigation: Use approved secret handling or SSH keys, avoid production server passwords, and review upload commands before execution.

Risk: Disabling SSH host verification can connect the upload flow to an unexpected host.

Mitigation: Require SSH host verification and approve the destination host before any demo upload.

Risk: Hardcoded group IDs, domains, and footer branding can send reports or demos to unintended third-party destinations.

Mitigation: Replace reporting targets, preview domains, and branding with explicitly approved values before sending reports or uploading demos.

## Reference(s):

- [Workflow Guide](references/workflow-guide.md)
- [Idea Content Specification](references/idea-content-spec.md)
- [Idea Template](references/idea-template.md)
- [PRD Design Specification](references/prd-design-spec.md)
- [PRD Template](references/prd-template.md)
- [Report Template Specification](references/report-template-spec.md)
- [Step-by-Step Report Specification](references/step-by-step-report-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, HTML/CSS/JavaScript files, shell commands, and short status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates three dated idea workspaces with idea notes, PRDs, demo files, preview URLs, and staged report messages.]

## Skill Version(s):

1.1.1 (source: server release evidence, created 2026-05-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
