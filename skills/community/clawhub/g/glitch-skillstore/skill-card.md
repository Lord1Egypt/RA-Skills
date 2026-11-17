## Description:

Search, install, and create OpenClaw skills with intelligent matching across known, local, and GitHub repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to find matching skills, inspect known or installed skills, install selected GitHub-hosted skills, and scaffold new skill directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unverified GitHub-hosted skills.

Mitigation: Review the selected repository before installation and prefer pinned, trusted sources.

Risk: The skill can write files outside the intended skill area when creating new skills from untrusted or path-like names.

Mitigation: Avoid untrusted names, reject path-like input, and stage generated files for review before use.

Risk: The bundled guidance may introduce broad behavioral preferences into generated skills.

Mitigation: Review generated skill documentation and remove behavioral rules that are unrelated to the skill's purpose.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chris6970barbarian-hue/skills/glitch-skillstore)
- [Publisher Profile](https://clawhub.ai/user/chris6970barbarian-hue)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Terminal text, Markdown skill files, JavaScript code, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write new skill directories and clone selected GitHub repositories when the user chooses those actions.]

## Skill Version(s):

2026.2.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
