## Description:

The directory for AI agent services, helping agents discover tools, platforms, and infrastructure built for agent integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to find agent-oriented services, inspect service metadata, and retrieve service skill.md files before deciding how to integrate them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched service skill.md content can change outside this release and may contain unsafe instructions.

Mitigation: Treat fetched service content as untrusted evidence; review it before following instructions or allowing credential use, file access, command execution, or further network transmission.

Risk: Using the skill sends requested service URLs to SkillBoss and requires a SKILLBOSS_API_KEY.

Mitigation: Use the skill only when sending those URLs to SkillBoss is acceptable, and scope the API key according to the deployment's credential policy.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/godferylindsay/skills/martin-agent-directory)
- [Publisher profile](https://clawhub.ai/user/godferylindsay)
- [Agent Directory homepage](https://ctxly.com)
- [SkillBoss setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python API examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for SkillBoss API calls.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
