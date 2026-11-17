## Description:

Dropbox Sign (sign.dropbox.com). Use this skill for ANY Dropbox Sign request — searching and reading data. Whenever a task involves Dropbox Sign, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Dropbox Sign account can retrieve account settings and search or read accessible signature requests and templates through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unchecked installer code.

Mitigation: Review and approve CLI installation separately, verify a fixed release, and consider installing from a trusted source.

Risk: Automatic skill synchronization may introduce undisclosed changes to agent skills.

Mitigation: Consider disabling automatic synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: The connected OOMOL account brokers access to private Dropbox Sign records.

Mitigation: Connect only the account needed for the requested reads and understand its access to private records.

## Reference(s):

- [Dropbox Sign](https://sign.dropbox.com)
- [Dropbox Sign API documentation](https://developers.hellosign.com/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance, Shell commands]

**Output Format:** [JSON connector responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results depend on the connected Dropbox Sign account's access; responses may contain private records.]

## Skill Version(s):

1.0.4 (source: frontmatter; server release 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
