## Description:

Write, review, or improve prompts for MindStudio Generate Text blocks, including plain text, structured JSON, variable injection, conditional logic, and dot-notation data access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sol1986](https://clawhub.ai/user/sol1986)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and MindStudio workflow builders use this skill to draft and review Generate Text block prompts with exact workflow variables, output settings, JSON schemas, sample outputs, and downstream dot-notation examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead generation or contact enrichment workflows may process unnecessary personal data.

Mitigation: Redact secrets and unnecessary personal data, and avoid unauthorized contact enrichment before using generated prompts in those workflows.

Risk: Prompts that process scraped webpages can be exposed to prompt injection or unreliable page content.

Mitigation: Add explicit prompt-injection defenses and human review before connecting scraped-page outputs to downstream automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sol1986/skills/mindstudio-generate-text-block-prompting-skill)
- [README](artifact/README.md)
- [Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, configuration guidance]

**Output Format:** [Markdown prompts, JSON schema examples, realistic sample outputs, and concise block-setting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided MindStudio variable names and workflow context.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
