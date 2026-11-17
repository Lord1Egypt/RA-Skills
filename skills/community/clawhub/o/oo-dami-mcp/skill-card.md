## Description:

DAMI (tikclubs.com). Use this skill for ANY DAMI request — reading, creating, updating, and deleting data. Whenever a task involves DAMI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the skill to inspect DAMI action schemas and work with TikTok Shop products, creators, competitors, and creator outreach through an authorized DAMI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes remote code whose exact local effects were unavailable for inspection, including automatic installation of other agent skills.

Mitigation: Review and install the CLI separately before enabling the skill.

Risk: DAMI outreach actions can incur costs, contact creators, or change workflow settings.

Mitigation: Use a narrowly authorized DAMI connection and review recipients, costs, and workflow changes when approving actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [DAMI homepage](https://www.tikclubs.com/)
- [DAMI API documentation](https://vnfrxfa5wp.feishu.cn/wiki/UpXTwU4vJiWBPmk3iY5cY7HAnSg)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Guidance with inline shell commands and JSON payloads; DAMI action responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill inspects each action's live schema before constructing its JSON payload.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
