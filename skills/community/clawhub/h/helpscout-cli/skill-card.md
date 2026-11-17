## Description:

CLI for the HelpScout API. Manage conversations, customers, mailboxes, knowledge base articles, and more from the terminal. Covers both Inbox and Docs APIs with full CRUD, PII redaction, permissions, and multiple output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmorse](https://clawhub.ai/user/rmorse)

### License/Terms of Use:


## Use Case:

Developers and support operations teams use this skill to manage Help Scout Inbox and Docs resources from an agent-assisted terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad write and delete access to Help Scout support data.

Mitigation: Configure a restrictive permissions allowlist, prefer read-only scopes, and require explicit human approval for write, delete, webhook, workflow, and self-update commands.

Risk: Credentials and debug output can expose sensitive Help Scout account data.

Mitigation: Use OS keyring or config-based credential storage, avoid passing secrets directly on the command line, and do not share raw debug logs.

Risk: Customer and user PII may be returned by Inbox commands.

Mitigation: Keep PII redaction enabled and require explicit approval before using unredacted output.

## Reference(s):

- [Help Scout skill page](https://clawhub.ai/rmorse/skills/helpscout-cli)
- [hs CLI homepage](https://github.com/operator-kit/hs-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include table, JSON, full JSON, or CSV output format guidance for hs CLI commands.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
