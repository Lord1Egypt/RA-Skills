## Description:

Documentation-only master skill for GLM ecosystem discovery and installation, providing a curated list of official GLM skills, install methods, and source links without executing scripts or subprocess commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this guide-only skill to discover GLM OCR, image, and vision skills, choose an installation path, and find downstream setup links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance uses unpinned ClawHub commands that can fetch current remote code.

Mitigation: Prefer a pinned clawhub version and inspect downstream skills before installing them.

Risk: Bulk-install guidance can install many downstream GLM skills at once.

Mitigation: Install only the specific downstream skills needed for the task and review each selected skill before use.

Risk: Downstream GLM skills may require ZHIPU_API_KEY credentials.

Mitigation: Use limited-scope API keys, avoid exposing unnecessary credentials, and keep keys out of source control.

## Reference(s):

- [GLM-Master-Skill Source](https://github.com/zai-org/GLM-skills/tree/main/skills/glm-master-skill)
- [GLM-5](https://github.com/zai-org/GLM-5)
- [GLM-OCR](https://github.com/zai-org/GLM-OCR)
- [GLM-Image](https://github.com/zai-org/GLM-Image)
- [GLM-V](https://github.com/zai-org/GLM-V)
- [BigModel API Docs](https://docs.bigmodel.cn/)
- [ClawHub Skill Page](https://clawhub.ai/jaredforreal/skills/glm-master-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; the skill itself does not execute commands or read credentials.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
