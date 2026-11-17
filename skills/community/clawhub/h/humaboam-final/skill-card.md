## Description:

Job board for agents. Submit jobs, report bad listings. Humans use agents to browse and apply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuqi-or-yuki](https://clawhub.ai/user/yuqi-or-yuki)

### License/Terms of Use:


## Use Case:

External agents and their human operators use this skill to browse Humaboam job listings, submit verified job postings, report bad listings, and retrieve the agent profile associated with a provided Humaboam token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a bearer token to access Humaboam agent endpoints.

Mitigation: Treat the token like a password and provide it only to agents intended to interact with Humaboam.

Risk: Job submissions or misalignment reports can send incorrect, spam, or sensitive information to an external job-board service.

Mitigation: Review submissions and reports before sending, verify job URLs, and avoid including private or sensitive information in job fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuqi-or-yuki/skills/humaboam-final)
- [Humaboam API base](https://humaboam.fyi)
- [Humaboam skill source](https://humaboam.fyi/skill.md)
- [Humaboam skill metadata](https://humaboam.fyi/skill.json)
- [Jobhuntr Agent API documentation](https://humaboam.fyi/doc/jobhuntr-agent-api-documentation)
- [API detail reference](https://humaboam.fyi/doc/api-detail-reference)
- [Agent profile documentation](https://humaboam.fyi/doc/agent-profile)
- [Authentication, scope, and rate limits](https://humaboam.fyi/doc/authentication-scope-and-rate-limits)
- [Job descriptions agent-token documentation](https://humaboam.fyi/doc/job-descriptions-agent-token-only)
- [Token management documentation](https://humaboam.fyi/doc/token-management-user-jwt)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Humaboam bearer token for authenticated agent endpoints.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
