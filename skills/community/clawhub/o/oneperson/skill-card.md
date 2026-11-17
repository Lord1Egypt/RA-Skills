## Description:

Your personal AI assistant platform - multi-agent orchestration, task management, and autonomous workflow execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyanhui](https://clawhub.ai/user/shiyanhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use OnePerson to connect an agent to the 1Person service for multi-agent orchestration, autonomous task management, reusable workflows, and persistent context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ONEPERSON_API_KEY is a secret credential and could enable unauthorized access if exposed.

Mitigation: Store the key in a secret manager or protected environment variable, avoid committing it to source control, and rotate it if exposure is suspected.

Risk: Tasks and context sent to 1Person may include sensitive information, and the service description includes persistent memory.

Mitigation: Review 1Person's data handling behavior before sensitive use and limit submitted context to information approved for that service.

Risk: Autonomous workflows can act on delegated tasks beyond the user's immediate view.

Mitigation: Review planned workflows, permissions, and outputs before relying on them for important work.

## Reference(s):

- [1Person Homepage](https://1person.pro)
- [1Person Documentation](https://docs.1person.pro)
- [ClawHub Skill Page](https://clawhub.ai/shiyanhui/skills/oneperson)
- [Publisher Profile](https://clawhub.ai/user/shiyanhui)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown guidance with environment variable setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ONEPERSON_API_KEY.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
