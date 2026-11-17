## Description:

Hersona applies reusable persona attributes to an agent session, blends compatible personality, speech, archetype, visual, and hobby templates, and can export or persist the resulting persona profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiro-0x](https://clawhub.ai/user/shiro-0x)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Hersona when they want an agent to adopt, test, measure, export, or persist a persona assembled from generic attributes rather than a named character. It supports short session-only persona trials, blended personas, persistent profile setup, recommendation flows, and interop exports for other agent frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change persona and system-prompt behavior across a session or persist it across future sessions.

Mitigation: Review the selected attributes, generated SOUL.md, and config.yaml changes before and after persistent or reset operations; test persona changes in single or multi mode before persistence.

Risk: The memory options can persist user-provided context and may capture sensitive information if used carelessly.

Mitigation: Do not place secrets, credentials, private conversation text, or sensitive personal data in --memory or --memory-file; keep memory entries minimal and review them before persistence.

Risk: Some documented shell and git workflows can be disruptive if run directly in an active workspace.

Mitigation: Use safer verification steps and backups before running evaluation recipes or destructive git commands, especially reset operations.

## Reference(s):

- [ClawHub Hersona Skill Page](https://clawhub.ai/shiro-0x/skills/hersona)
- [Server-Resolved GitHub Source](https://github.com/shiro-0x/hersona/tree/main/skills/hersona)
- [Hersona Project Homepage](https://github.com/shiro-0x/hersona)
- [Artifact Reference](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/messages exports, and YAML or profile configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent profile content, SOUL.md memory sections, persona registry snippets, and deterministic measurement or recommendation reports.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
