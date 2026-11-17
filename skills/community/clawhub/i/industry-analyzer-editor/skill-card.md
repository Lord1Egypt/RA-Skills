## Description:

Aggregates four industry-analysis dimension outputs into one comprehensive Markdown report with an executive summary, chapter synthesis, cross-dimension insights, and audience-specific recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of the industry-analysis pipeline use this skill after the four upstream analysis steps complete to synthesize a final industry report. It is also used to regenerate the report when upstream Markdown files are updated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rerunning the skill overwrites the generated main report and updates local pipeline state.

Mitigation: Confirm the four upstream Markdown files and session.json are the intended versions before rerunning the synthesis step.

## Reference(s):

- [Synthesis template](references/synthesis-template.md)
- [ClawHub skill page](https://clawhub.ai/zrxparley/skills/industry-analyzer-editor)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown report plus session.json status update]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes output/{industry-slug}/industry-analysis-report.md and marks status.report as done.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
