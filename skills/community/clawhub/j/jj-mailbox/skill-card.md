## Description:

Send and receive messages between AI agents using jj (Jujutsu) version control as a file-based mailbox. Enables cross-machine agent collaboration with zero infrastructure beyond a git remote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miaodx](https://clawhub.ai/user/miaodx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multiple AI agents through JSON messages stored in a shared jj-backed mailbox repository. It supports local collaboration and opt-in cross-machine synchronization through a configured git remote.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated agent names may allow file reads, writes, or moves outside the declared mailbox directory.

Mitigation: Use only trusted mailbox repositories and trusted agent names, avoid sensitive directories, and prefer a fixed version that rejects traversal, absolute paths, and symlink escapes before file operations.

Risk: Opt-in multi-machine synchronization can push mailbox contents to the configured git remote using host-level git or SSH credentials.

Mitigation: Start synchronization only with trusted remotes and keep secrets, credentials, and sensitive data out of the mailbox repository.

## Reference(s):

- [Jujutsu installation documentation](https://jj-vcs.dev/docs/install/)
- [ClawHub skill page](https://clawhub.ai/miaodx/skills/jj-mailbox)
- [ClawHub publisher profile](https://clawhub.ai/user/miaodx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON message examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jj-mailbox, jj, git, and python3; uses JJ_MAILBOX_REPO, JJ_MAILBOX_AGENT, and JJ_MAILBOX_INTERVAL environment variables.]

## Skill Version(s):

0.1.3 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
