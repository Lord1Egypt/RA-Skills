## Description:

Create project timeline visualizations for grant proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Grant writers, researchers, and project teams use this skill to turn project milestones and timelines into grant proposal timeline artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user-specified output path can overwrite any writable file available to the process.

Mitigation: Run the skill in a constrained workspace, provide explicit safe output paths, and avoid paths influenced by untrusted data until output path validation is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/grant-gantt-chart-gen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Shell commands]

**Output Format:** [Plain text, Mermaid Gantt syntax, JSON, or saved chart files depending on selected format and output path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print timeline summaries and write generated output to a user-specified file path.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
