## Description:

Adds mind maps and architecture diagrams to Markdown documents when users request a mind map, architecture diagram, or chart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drunkpig](https://clawhub.ai/user/drunkpig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to create and embed mind map or architecture diagram assets alongside Markdown documentation, with generated PNGs and source files kept in a local .mddoc directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install mddoc-cli globally from npm if the dependency is missing.

Mitigation: Prefer manually installing reviewed, pinned dependencies or running the skill in a contained project environment.

Risk: The skill runs local diagram rendering commands and creates .mddoc source and PNG files.

Mitigation: Review proposed file paths and generated diagram sources before execution, especially in shared repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drunkpig/skills/mddoc-design)
- [D2 installation documentation](https://d2lang.com/tour/install)
- [Project issue tracker](https://github.com/drunkpig/md-of-programer/issues)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and diagram source snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [.mddoc source files and PNG outputs are created alongside the target Markdown file when the agent follows the skill.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
