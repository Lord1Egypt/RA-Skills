## Description:

为 OpenClaw AI Agent 生成完整的角色化龙虾灵魂方案，包括身份定位、SOUL.md/IDENTITY.md 内容、底线规则、命名和头像提示词。

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent builders use this skill to design a persona-driven lobster agent, either through guided choices or randomized gacha output. The skill helps produce role identity, character boundaries, names, avatar prompts, and optional SOUL.md and IDENTITY.md files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write SOUL.md and IDENTITY.md after user confirmation, which could overwrite existing persona files in the chosen directory.

Mitigation: Confirm the exact target directory and whether existing SOUL.md or IDENTITY.md files should be replaced before allowing writes.

Risk: The optional avatar workflow depends on a separate baoyu-image-gen skill that is outside this release.

Mitigation: Review and install the image-generation dependency separately; if unavailable or unsuitable, use the emitted avatar prompt text manually.

Risk: The avatar prompt workflow describes writing prompts to predictable /tmp paths.

Mitigation: Prefer a safe temporary path when handling avatar prompts, especially on shared systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eamanc-lab/skills/openclaw-persona-forge)
- [Project Homepage](https://github.com/eamanc-lab/openclaw-persona-forge)
- [baoyu-image-gen Optional Dependency](https://github.com/JimLiu/baoyu-skills)
- [Adam Avatar Style Reference](https://raw.githubusercontent.com/eamanc-lab/openclaw-persona-forge/main/docs/adam-claw-logo.png)
- [avatar-style.md](references/avatar-style.md)
- [boundary-rules.md](references/boundary-rules.md)
- [error-handling.md](references/error-handling.md)
- [identity-tension.md](references/identity-tension.md)
- [naming-system.md](references/naming-system.md)
- [output-template.md](references/output-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown text with optional generated SOUL.md and IDENTITY.md files, shell command output from the gacha script, and avatar prompt text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally call a separate image-generation skill when installed; otherwise returns avatar prompts for manual use.]

## Skill Version(s):

2.2.0 (source: evidence.release.version; artifact frontmatter metadata lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
