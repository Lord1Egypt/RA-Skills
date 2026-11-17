## Description:

Use Mailosaur through an OOMOL-connected account to read, search, create, update, and delete email testing servers and messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA teams use this skill to inspect Mailosaur inboxes, search and retrieve test messages, manage servers, and review account usage through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs execution of remote installers, and the deployed CLI and broader agent changes were not verified.

Mitigation: Review installation instructions and prefer a pinned, inspected CLI installation; decide whether to allow startup skill synchronization, which the documentation says can be disabled with OO_SKILLS_SYNC_DISABLED.

Risk: Mailosaur write and destructive actions can change or remove account data.

Mitigation: Use an appropriately limited connection and keep the skill's confirmation steps for write and destructive actions.

## Reference(s):

- [Mailosaur API documentation](https://mailosaur.com/docs/api)
- [Mailosaur](https://mailosaur.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payload examples; connector responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector actions include reads, writes, and destructive operations; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
