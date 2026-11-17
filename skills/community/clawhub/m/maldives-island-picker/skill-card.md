## Description:

Helps users choose Maldives resort islands by collecting travel preferences, searching travel guidance, checking Fliggy product availability, and producing a structured island-selection report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miracleaaa](https://clawhub.ai/user/miracleaaa)

### License/Terms of Use:

MIT-0

## Use Case:

External travel-planning users and agents use this skill to narrow Maldives resort choices from a user's trip type, priorities, transportation preference, and budget, then produce a decision-ready recommendation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run an unpinned external npm CLI for travel product lookup.

Mitigation: Pin or pre-approve the CLI version before use, and review the command before execution.

Risk: The skill defaults to saving generated reports into the active workspace.

Mitigation: Confirm the target filename and location before file creation, especially in workspaces with important existing files.

Risk: PDF export processes Markdown content and should only be used with trusted inputs.

Mitigation: Run the PDF exporter only on trusted Markdown in a restricted environment with reviewed dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miracleaaa/skills/maldives-island-picker)
- [Intent collection reference](references/intent-collection.md)
- [Report template](references/report-template.md)
- [Fliggy](https://www.fliggy.com/)
- [Ctrip](https://www.ctrip.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown report with tables, product links, images, source notes, optional shell commands, and optional PDF export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to saving a dated Markdown report in the active workspace; PDF export is available when requested and dependencies are installed.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
