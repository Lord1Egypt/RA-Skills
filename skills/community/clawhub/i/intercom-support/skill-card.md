## Description:

Manage Intercom workspaces for customer support. Handle conversations, contacts, companies, tickets, and help center content. Automate replies, assign conversations to teams, manage articles, and track team performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Support, customer success, and operations teams use this skill to manage Intercom conversations, contacts, companies, tickets, help center content, transcripts, exports, and workspace administration through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external OAuth-backed ClawLink plugin with access to customer support data.

Mitigation: Install and connect it only when the user trusts ClawLink and the plugin, and verify how to revoke the OAuth connection and remove the plugin before use.

Risk: Intercom operations may expose conversations, contacts, tickets, help-center content, transcripts, and exports.

Mitigation: Use a least-privilege Intercom account and confirm the target workspace, resource, and intended effect before any write, delete, export, or conversation state-change action.

## Reference(s):

- [Intercom API Documentation](https://developers.intercom.com/)
- [Intercom Articles API](https://developers.intercom.com/reference/list-articles)
- [Intercom Conversations API](https://developers.intercom.com/reference/conversations)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawHub skill page](https://clawhub.ai/hith3sh/skills/intercom-support)
- [ClawHub publisher profile](https://clawhub.ai/user/hith3sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for Intercom actions and requires explicit confirmation before write, delete, export, or conversation state-change operations.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
