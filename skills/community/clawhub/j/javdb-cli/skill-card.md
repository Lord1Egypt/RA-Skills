## Description:

Operate the installed JavDB CLI for discovery, authenticated lists, and explicitly authorized account, configuration, state, or preview asset actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flanchanxwo](https://clawhub.ai/user/flanchanxwo)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate the installed JavDB CLI for scoped discovery, authenticated list reading, account and configuration tasks, and explicitly authorized state changes or preview asset actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local authentication file contains usernames, passwords, and tokens.

Mitigation: Do not read, print, upload, or include the authentication file in diagnostics; handle login through a private interactive prompt.

Risk: Image search uploads the selected image to AVScan or a configured provider.

Mitigation: Use only an image the user has authorized for upload and explain that privacy effect before searching.

Risk: The security assessment is benign with medium confidence, and Skillspector coverage is partial because three references could not be resolved.

Mitigation: Review the unresolved references and whether self-updates fit the use case; authorize updates explicitly and retain the documented signature and checksum checks.

## Reference(s):

- [Project homepage](https://github.com/FlanChanXwO/javdb-cli)
- [Authentication and Accounts](references/auth.md)
- [Discovery and Navigation](references/discover.md)
- [Installation and Updates](references/install.md)
- [Preview Media Assets](references/media.md)
- [Explicit State Changes](references/state.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, NDJSON, Files]

**Output Format:** [Markdown guidance with shell command examples; command results may be text, JSON, or NDJSON, with preview asset files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output shape depends on the selected command; preview asset files are saved only for explicitly requested downloads.]

## Skill Version(s):

0.8.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
