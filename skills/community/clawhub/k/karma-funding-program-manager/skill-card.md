## Description:

Create and manage Karma funding programs, including registry setup, intake forms, applications, reviewers, milestones, payouts, grant agreements, and AI evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maheshmurthy](https://clawhub.ai/user/maheshmurthy)

### License/Terms of Use:

MIT-0

## Use Case:

Program operators, grant administrators, reviewers, and applicants use this skill to create Karma funding programs, configure application intake, manage review workflows, submit applications, and coordinate payouts and agreements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform high-impact funding administration actions, including approvals, payouts, reviewer changes, agreement signatures, and AI evaluation submissions.

Mitigation: Manually confirm those actions before sending authenticated API requests.

Risk: The skill uses Karma API keys and may persist credentials in plaintext shell or plugin data files.

Mitigation: Use session-only credentials or secure secret storage, and only provide API keys you are willing to grant to the agent.

Risk: The API host can be overridden with KARMA_API_URL.

Mitigation: Leave the default Karma endpoint unless you fully trust the alternate endpoint.

## Reference(s):

- [Karma API Documentation](https://gapapi.karmahq.xyz/v2/docs/static/index.html)
- [ClawHub Skill Listing](https://clawhub.ai/maheshmurthy/skills/karma-funding-program-manager)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown guidance with inline bash curl commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow prompts, endpoint-specific payload guidance, and operational checks for Karma funding program administration.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
