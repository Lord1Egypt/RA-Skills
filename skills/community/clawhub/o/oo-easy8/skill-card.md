## Description:

Use this skill to read and manage Easy8 projects and tasks through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents working with Easy8 use this skill to retrieve projects and tasks or create, update, and delete them through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote software and introduce broader agent changes without separate consent.

Mitigation: Approve CLI installation separately, use a verified release, and review or disable automatic skill synchronization before running the skill.

Risk: Write and delete actions can change or permanently remove Easy8 data.

Mitigation: Connect only the intended Easy8 account and confirm the exact effect and target before approving write or destructive actions.

## Reference(s):

- [Easy8](https://www.easy8.com)
- [Easy8 API Documentation](https://developers.easy8.com/APIs/REST-like-API/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Easy8 ClawHub Skill](https://clawhub.ai/oomol/skills/oo-easy8)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON payload and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions vary by connector schema; responses may contain Easy8 project and task data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
