## Description:

Manage Nginx Proxy Manager (NPM) hosts, certificates, and access lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weird-aftertaste](https://clawhub.ai/user/weird-aftertaste)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect Nginx Proxy Manager proxy hosts and certificates, enable or disable hosts, and manage existing proxy-host records through the NPM API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses live Nginx Proxy Manager admin credentials and stores an API token on disk.

Mitigation: Use only with a trusted NPM instance over HTTPS, prefer a least-privilege account if available, avoid shared environments, and protect or clear /root/.npm-token.json after use.

Risk: The delete command can immediately remove proxy-host configuration without a built-in confirmation or dry run.

Mitigation: Review the target host ID before running destructive actions and confirm the current host details first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weird-aftertaste/skills/npm-proxy)
- [Publisher profile](https://clawhub.ai/user/weird-aftertaste)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print tabular host and certificate summaries or formatted JSON returned by the NPM API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
