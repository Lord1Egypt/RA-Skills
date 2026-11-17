## Description:

Mind Layer helps an AI assistant organize identity, rules, user preferences, long-term memory, daily reflections, and archive routines into a six-layer memory framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z44264677](https://clawhub.ai/user/z44264677)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up persistent memory files, communication rules, and reflection templates for an OpenClaw assistant. It is intended for agents that need structured recall of user preferences, decisions, lessons, and daily activity summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent cross-session memory and broad behavioral instructions that can affect future agent behavior.

Mitigation: Keep memory files in a dedicated, reviewable namespace and confirm each persistent write before it becomes authoritative.

Risk: Persistent memory files could retain sensitive personal information or secrets if users store them there.

Mitigation: Do not store secrets, credentials, health, financial, or highly sensitive personal information; periodically delete stale records.

Risk: Installing with a moving latest tag can change the skill content between installs.

Mitigation: Prefer a pinned installer version instead of clawhub@latest when deploying the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/z44264677/skills/mind-layer)
- [README](artifact/README.md)
- [Skill Overview](artifact/SKILL.md)
- [Communication Rules](artifact/rules/RULES.md)
- [Core Principles](artifact/rules/principles.md)
- [Identity Template](artifact/templates/identity.md)
- [Memory Template](artifact/templates/memory.md)
- [Daily Reflection Template](artifact/templates/daily.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance, Shell commands]

**Output Format:** [Markdown instructions, templates, file layout guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent memory and rule-file guidance for an agent workspace; users should review writes before making them authoritative.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
