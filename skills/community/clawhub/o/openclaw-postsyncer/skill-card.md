## Description:

Manage your PostSyncer social media workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abakermi](https://clawhub.ai/user/abakermi)

### License/Terms of Use:


## Use Case:

Developers and social media operators use this skill to configure PostSyncer access, list workspaces and posts, and create basic text posts from an agent-assisted workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The create-post command can affect a connected PostSyncer account.

Mitigation: Review workspace IDs and post text before running account-impacting commands.

Risk: The skill documents PostSyncer CLI usage but does not include the CLI implementation.

Mitigation: Verify the postsyncer CLI source before allowing an agent to use it.

Risk: The skill requires POSTSYNCER_API_KEY for account access.

Mitigation: Install only when agent access to the intended PostSyncer account is acceptable.

## Reference(s):

- [PostSyncer Settings](https://app.postsyncer.com/settings)
- [ClawHub skill page](https://clawhub.ai/abakermi/skills/openclaw-postsyncer)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POSTSYNCER_API_KEY for PostSyncer account access.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
