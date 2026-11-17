## Description:

Helps agents manage Mailchimp audiences, subscribers, campaigns, templates, automations, and reports through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and developers use this skill to inspect Mailchimp account data and, with approval, manage subscribers, campaigns, and related email marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Maton gateway accesses the connected Mailchimp account.

Mitigation: Use a connection with only the access needed for the task and prefer CLI/OAuth login over raw API keys.

Risk: Writes and campaign sends can alter subscriber data or send real email.

Mitigation: Review the target and intended effect, and obtain explicit approval before each action.

Risk: Deployed functions, triggers, and destinations can keep running or forwarding events.

Mitigation: Approve each deployment and destination separately, and remove unused connections and automations when finished.

## Reference(s):

- [Mailchimp skill on ClawHub](https://clawhub.ai/byungkyu/skills/mailchimp)
- [Maton](https://maton.ai)
- [Mailchimp Marketing API documentation](https://mailchimp.com/developer/marketing/)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.5 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
