## Description:

Connects agents to Notion for reading, creating, updating, and deleting workspace content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Notion account can search and read workspace content, manage pages and databases, and work with comments and views through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute changing remote software without asking for installation approval.

Mitigation: Review CLI setup before running it, prefer a verified fixed release, and check whether automatic installation of other agent skills is enabled.

Risk: The Notion connection may have access beyond the content needed for a task.

Mitigation: Limit the connection to the Notion content needed for the task.

Risk: Write and destructive actions can change or remove Notion content.

Mitigation: Retain the skill's required confirmations for changes, and confirm the exact target and effect before destructive actions.

## Reference(s):

- [Notion API documentation](https://developers.notion.com/)
- [Notion](https://www.notion.so)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Notion skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-notion)

## Skill Output:

**Output Type(s):** [API calls, Guidance]

**Output Format:** [Notion workspace actions and concise text or Markdown results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require inputs that match the live connector schema; results depend on the connected account's access and capabilities.]

## Skill Version(s):

1.0.7 (source: server-resolved release and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
