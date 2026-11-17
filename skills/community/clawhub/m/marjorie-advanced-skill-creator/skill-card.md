## Description:

Advanced OpenClaw skill creation handler that executes the official 5-step research flow with comprehensive analysis and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or modify OpenClaw, Moltbot, or ClawDBot skills with structured research, comparison, security considerations, and complete SKILL.md output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill-creation prompts may be sent to the third-party SkillBoss/HeyBossAI service.

Mitigation: Do not include secrets, private code, customer data, credentials, or internal system details in requests.

Risk: Generated recommendations may be template-based output rather than verified current research.

Mitigation: Review generated skills, verify cited standards or examples, and scan outputs before deployment.

## Reference(s):

- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [ClawdBot skills documentation](https://docs.clawd.bot/tools/skills)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot)
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/marjorie-advanced-skill-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with complete SKILL.md content, directory previews, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call SkillBoss API Hub when SKILLBOSS_API_KEY is configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
