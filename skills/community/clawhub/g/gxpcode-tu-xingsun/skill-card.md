## Description:

Tracks pharmaceutical regulations from configured web and RSS sources, analyzes relevance to a user profile, and produces regulation tracking reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxpcode-hezhong](https://clawhub.ai/user/gxpcode-hezhong)

### License/Terms of Use:

MIT-0

## Use Case:

Regulatory affairs and quality teams use this skill to monitor pharmaceutical regulation sources, compare new items against history, fetch details and attachments, analyze applicability, and generate Markdown/PDF tracking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup installs mutable third-party dependencies and browser components.

Mitigation: Review setup before installation, use a virtual environment, pin dependencies with hashes, and use trusted package and browser download sources.

Risk: New-source analysis can persistently change monitored sources and parser code based on broad web inputs.

Mitigation: Require human review for new-source analysis, parser changes, and updates to configured regulatory sources before running the tracking workflow.

Risk: The source manager can persistently change which regulatory domains are monitored.

Mitigation: Restrict source-management access and maintain an allowlist of approved regulatory domains.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gxpcode-hezhong/skills/gxpcode-tu-xingsun)
- [Configured regulatory sources](artifact/resources/sources.yaml)
- [Workflow definition](artifact/SKILL.md)
- [Report generation step](artifact/resources/steps/step_5.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, YAML configuration, shell commands, and generated Markdown/PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured web and RSS sources, local history for duplicate detection, and optional PDF attachment/report outputs in the workspace.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
