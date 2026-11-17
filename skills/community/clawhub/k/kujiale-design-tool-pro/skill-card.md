## Description:

酷家乐设计-专业版 helps enterprise interior design teams compare multiple design proposals, batch render high-resolution images and panoramas, manage custom style libraries, and collaborate on versioned plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

Proprietary

## Use Case:

External design teams and enterprise interior designers use this skill to guide commercial design workflows for multi-style proposal generation, batch rendering, panorama export, and team-based plan versioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enterprise Kujiale credentials may be exposed through repo-tracked configuration files.

Mitigation: Keep tokens out of tracked files and store them in environment variables or a managed secret store.

Risk: Broad command and file authority can affect local files or invoke external design workflows.

Mitigation: Require explicit confirmation before running referenced scripts, approving team changes, or writing generated renders and reports.

Risk: Generated renders, reports, and exports may be written outside the intended workspace.

Mitigation: Use restricted output directories and review paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/kujiale-design-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured status, result, log, and error fields for design workflow responses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
