## Description:

Search and answer questions over documents already uploaded to NotebookLM using the nlm CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lhquangit](https://clawhub.ai/user/lhquangit)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query existing NotebookLM notebooks from an agent runtime, including Telegram-triggered workflows, and return concise answers grounded in NotebookLM results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Google and NotebookLM session cookies that can grant access to notebook content.

Mitigation: Use a dedicated low-privilege Google account or profile, protect cookie files and secrets, and rotate cookies when access changes.

Risk: Bundled setup scripts can perform privileged VPS changes, package installs, OpenClaw config edits, group changes, and optional systemd integration.

Mitigation: Review scripts before installation, avoid running the bootstrap as root unless those changes are acceptable, and prefer a pinned, least-privilege manual setup for production environments.

Risk: Exposing the Telegram /nlm workflow to untrusted users can allow unintended NotebookLM queries.

Mitigation: Limit access to trusted Telegram users and review NotebookLM CLI actions before enabling the workflow on a shared runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lhquangit/skills/notebooklm-cli-cookies)
- [VPS installation guide](artifact/docs/GUIDELINE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include NotebookLM notebook identity, query results, setup guidance, and troubleshooting steps.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
