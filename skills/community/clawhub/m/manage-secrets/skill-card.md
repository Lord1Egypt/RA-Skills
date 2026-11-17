## Description:

Set or update environment secrets via the set-secret GitHub Actions workflow when a user asks to update, rotate, or set a secret, token, or API key for this persona's environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aehrt55](https://clawhub.ai/user/aehrt55)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized operators use this skill to trigger a GitHub Actions workflow that updates SOPS-encrypted environment secrets for a persona and monitors the workflow run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill manages deployment secrets and depends on a GitHub token with Actions write permission.

Mitigation: Install only in tightly controlled environments with a minimally scoped token, trusted operators, and verified workflow-side RBAC.

Risk: Secret values may be supplied directly to shell commands and workflow dispatch inputs.

Mitigation: Use logging redaction, avoid exposing secret values in command-line history or logs, and prefer revising the workflow path to avoid raw command-line secret arguments.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENT_GITHUB_PAT and MANAGE_SECRETS_GITHUB_REPO environment variables; secret keys must use uppercase environment-variable format.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
