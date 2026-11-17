## Description:

Use the OpenPond CLI to create repos, watch deployments, and run tools without the web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucrypto](https://clawhub.ai/user/glucrypto)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate OpenPond apps from the command line, including creating repositories, pushing code, watching deployments, running tools, and managing account-level app workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or invoking the OpenPond CLI package can execute a package that has not been locally reviewed.

Mitigation: Verify that openpond-code is the intended package and prefer a pinned, reviewed version before installing or using npx.

Risk: OpenPond API keys or tokenized repository operations can expose account access if secrets are pasted into shell history, logs, or committed configuration.

Mitigation: Use interactive login, scoped environment injection, or a secret manager; keep credentials least-privileged and easy to revoke.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
