## Description:

Initializes paper-kb users by checking Feishu registration status, guiding first-time registration, creating a private Gitea knowledge-base repository, and coordinating Feishu Bitable setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Paper-kb operators and developers use this skill to onboard Feishu users into a personal research knowledge-base workflow. It checks registration state, collects a Gitea username and research direction, creates the user's private repository structure, and records Feishu Bitable identifiers when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on broad Gitea administrator access for user repository creation and shared configuration updates.

Mitigation: Review before installation, avoid a site-wide administrator token where possible, and restrict deployment to a controlled paper-kb environment.

Risk: The default Gitea endpoint is HTTP, which can expose tokens or user data on an untrusted network.

Mitigation: Move Gitea to HTTPS before configuring any production token or user workflow.

Risk: The account-linking flow accepts a Feishu user and requested Gitea account without built-in proof that the Feishu user controls that Gitea account.

Mitigation: Add an ownership proof step before binding a Feishu identity to a Gitea username.

Risk: Feishu table tokens and user mappings may be stored in users.json.

Mitigation: Protect or avoid storing Feishu tokens in users.json, and limit access to the system-config repository.

Risk: The setup script may install dependencies into the system Python environment.

Mitigation: Install dependencies in a dedicated virtual environment for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/init-user)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, shell commands, configuration guidance, and single-line JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the current Feishu open_id, Gitea username, research direction, and optional Feishu Bitable identifiers.]

## Skill Version(s):

2.1.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
