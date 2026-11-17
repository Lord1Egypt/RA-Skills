## Description:

Access Claude models through SkillBoss as an OpenAI-compatible API gateway using one SkillBoss API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and call Claude-family models through the SkillBoss API gateway without managing separate provider accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API credentials are sent to SkillBoss as a third-party gateway.

Mitigation: Use the skill only when the user intentionally wants SkillBoss and accepts that data handling path.

Risk: The setup path asks an agent to follow mutable external instructions.

Mitigation: Inspect and approve the remote setup steps before allowing an agent to run them.

Risk: The skill expands a Claude-focused workflow into access to a broader API surface.

Mitigation: Constrain use to the intended Claude API workflow unless the user explicitly requests broader SkillBoss APIs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/godfery-claude-api)
- [Publisher profile](https://clawhub.ai/user/godferylindsay)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [SkillBoss console](https://skillboss.co/console)
- [SkillBoss products](https://skillboss.co/products)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with bash, curl, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
