## Description:

Dynamic personality evolution for OpenClaw agents. Learn interaction patterns, adapt tone, and mode switching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngmeyer](https://clawhub.ai/user/ngmeyer)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to create adaptive agent personas, analyze interaction patterns, switch communication modes, and generate weekly suggestions for persona or SOUL.md updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command injection or unsafe execution from untrusted CLI arguments.

Mitigation: Run only a fixed reviewed release in a trusted workspace and do not pass untrusted input to the CLI.

Risk: Generated persona, memory-derived, and evolution files may contain sensitive personal profile data.

Mitigation: Keep PERSONA and memory-derived files private, and delete or exclude them from repositories, shared backups, and logs when they contain private information.

Risk: Automatic session analysis may create or update behavior suggestions that affect the agent's personality.

Mitigation: Review generated reports and suggested SOUL.md or PERSONA changes before adopting them.

Risk: Unpinned npx install examples can execute code that has not been reviewed for the target environment.

Mitigation: Prefer installing a pinned, reviewed version instead of running unpinned npx commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ngmeyer/skills/personality-dynamics)
- [OpenClaw persona-evolution repository](https://github.com/openclaw/persona-evolution)
- [OpenClaw persona-evolution issues](https://github.com/openclaw/persona-evolution/issues)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON files, shell command output, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates PERSONA files and evolution reports in the current workspace.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
