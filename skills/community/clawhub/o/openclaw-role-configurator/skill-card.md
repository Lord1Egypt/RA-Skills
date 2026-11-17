## Description:

Helps OpenClaw users configure or reconfigure an assistant role through guided prompts, bundled role templates, local SOUL.md generation, and related skill recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill during first-time setup or later role changes to choose an assistant persona, define its tasks and communication style, apply one of 21 bundled templates, and receive related skill recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the persistent SOUL.md assistant profile.

Mitigation: Review generated role text before applying it and keep the backup if rollback may be needed.

Risk: Some bundled templates cover health, pregnancy, newborn-care, and therapy-style use cases.

Mitigation: Use those templates only for general support and do not rely on them for medical or mental-health decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuqingsonga/skills/openclaw-role-configurator)
- [README](artifact/README.md)
- [Role templates](artifact/data/role_templates.json)
- [Skill recommendation rules](artifact/data/skill_recommendations.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance and generated SOUL.md configuration text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local SOUL.md role configuration file and create a backup of an existing SOUL.md file.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
