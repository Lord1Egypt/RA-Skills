## Description:

Access Overleaf projects via CLI for reading and writing LaTeX files, syncing local .tex files, downloading projects, managing project structure, and accepting project invitations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and writing teams use this skill to let an agent inspect, update, download, and synchronize Overleaf LaTeX projects through the pyoverleaf CLI and Python API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser session cookies and persistent keychain access to authenticate to Overleaf.

Mitigation: Review before installing, use a dedicated browser profile limited to Overleaf where practical, and confirm that agent access to the account is acceptable.

Risk: The skill can perform remote write, delete, download, and invite-acceptance actions on Overleaf projects.

Mitigation: Require explicit confirmation before any write, delete, download, or invite-acceptance action and review Overleaf history after changes.

Risk: The skill depends on pyoverleaf behavior for authenticated access and project operations.

Mitigation: Pin pyoverleaf to the audited version or independently verify the installed package before use.

## Reference(s):

- [ClawHub Overleaf Skill](https://clawhub.ai/easonc13/skills/overleaf)
- [pyoverleaf GitHub](https://github.com/jkulhanek/pyoverleaf)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands or code that read browser-authenticated Overleaf content or write changes to remote projects.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
