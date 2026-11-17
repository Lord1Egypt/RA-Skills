## Description:

Monitor specified GitHub repositories for new releases and receive notifications of newly detected tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogue-agent1](https://clawhub.ai/user/rogue-agent1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor selected GitHub repositories for newly published releases and receive concise status output suitable for scheduled checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted GitHub release data may lead to local command execution through the bundled release-check script.

Mitigation: Use only trusted repositories, review the script before installing, and avoid unattended scheduling until the interpolation issue is fixed.

Risk: The script relies on the caller's GitHub CLI authentication and local session permissions.

Mitigation: Run it with a least-privileged GitHub/session environment and limit access to only the repositories needed for release monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogue-agent1/skills/github-release-watcher)
- [Publisher profile](https://clawhub.ai/user/rogue-agent1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance with concise status text from the release-check script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a repos.txt configuration file and an authenticated GitHub CLI session.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
