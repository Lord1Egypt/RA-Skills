## Description:

Use AgentLine through an OOMOL-connected account to read, create, update, and delete voice agents and contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage AgentLine voice agents, contacts, and account voice settings through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute a downloaded CLI installer without a separately defined installation scope.

Mitigation: Install a verified CLI release yourself, or review the installer and its local changes and require approval before running it.

Risk: Deleting an agent permanently removes its associated calls, transcripts, messages, contacts, and webhook.

Mitigation: Confirm the target and obtain explicit user approval before deleting an agent; retain the skill's existing destructive-action confirmation.

## Reference(s):

- [AgentLine API documentation](https://docs.agentline.cloud/introduction)
- [AgentLine homepage](https://agentline.cloud)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON action results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
