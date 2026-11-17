## Description:

Use Formsite through an OOMOL-connected account to read, create, update, and delete form data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to read Formsite forms, items, results, and webhooks, and to create, update, or delete webhooks through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded installation code without asking for approval.

Mitigation: Install a reviewed, fixed CLI release before use and require approval for later installations or agent-skill changes.

Risk: The connected account may expose Formsite data, and webhook changes can alter integrations.

Mitigation: Use an authorized Formsite connection and require approval before creating, updating, or deleting webhooks.

## Reference(s):

- [Formsite API documentation](https://support.formsite.com/hc/en-us/articles/46181026038931-API)
- [Formsite](https://www.formsite.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and JSON payloads or returned data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Formsite form, result, item, or webhook data returned by requested actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
