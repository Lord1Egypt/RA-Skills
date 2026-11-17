## Description:

Creates, reads, edits, splits, combines, and quality-checks PowerPoint .pptx presentations using local presentation tooling and PPTX package workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinfeihaaaaaaaaaaa](https://clawhub.ai/user/yinfeihaaaaaaaaaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create new slide decks, inspect or extract content from existing .pptx files, and edit presentation templates while preserving Office package structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan summary says the setup and helper scripts reach beyond a narrow PPTX-only scope.

Mitigation: Install in a dedicated virtual environment with project-local npm dependencies and pinned versions.

Risk: The skill can run local Office conversion tools and modify presentation files.

Mitigation: Use a restricted workspace that excludes sensitive environment variables and unrelated documents, and work on copies of presentation files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinfeihaaaaaaaaaaa/skills/pptx-localized)
- [Publisher profile: yinfeihaaaaaaaaaaa](https://clawhub.ai/user/yinfeihaaaaaaaaaaa)
- [README.md](README.md)
- [Editing Presentations](editing.md)
- [PptxGenJS - Create Presentations from Scratch](pptxgenjs.md)
- [Anthropic official PPTX skill](https://github.com/anthropics/skills/tree/main/skills/pptx)
- [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and generated or modified .pptx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, modify, unpack, repack, and thumbnail presentation files in the workspace; visual QA can require LibreOffice and Poppler.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
