## Description:

Advanced Skill Creator helps agents create or modify OpenClaw, Moltbot, and ClawDBot skills by following a structured five-step research and output workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to draft or revise OpenClaw-compatible skill packages with frontmatter, examples, implementation guidance, and security considerations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill requests may be sent to a third-party AI API.

Mitigation: Avoid including secrets, private code, internal URLs, personal data, or other sensitive material in requests.

Risk: Generated skills may contain unsafe, incorrect, or overly broad instructions.

Mitigation: Manually review generated SKILL.md content and scan it before installing or publishing.

Risk: The artifact describes completed research steps that the included script may only simulate.

Mitigation: Verify cited documentation, public-skill comparisons, and best-practice claims before relying on the generated output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-advanced-skill-creator)
- [ClawdBot skills documentation](https://docs.clawd.bot/tools/skills)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML frontmatter examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call SkillBoss API Hub when SKILLBOSS_API_KEY is configured; generated skills should be manually reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
