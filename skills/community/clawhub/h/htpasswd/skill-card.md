## Description:

Generate htpasswd entries for Apache/Nginx basic auth password management. Use when creating credentials, managing password files, or verifying users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to create and manage Apache/Nginx basic-auth htpasswd files, including adding, deleting, listing, and verifying users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify real htpasswd authentication files.

Mitigation: Use it only on files explicitly named by the user, keep backups, and require confirmation before create, add, or delete operations on production authentication files.

Risk: Passwords are accepted as command-line arguments and may be exposed through shell history or process listings.

Mitigation: Prefer a safer password input path before production use and rotate any passwords already entered through command examples or shell history.

Risk: The default apr1 hash algorithm prioritizes compatibility over stronger hashing.

Mitigation: Set HTPASSWD_ALGO=sha512 where compatible with the target Apache or Nginx deployment.

Risk: Username handling requires review before use with production authentication files.

Mitigation: Use simple literal usernames only and avoid production files until username matching has been reviewed for literal handling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/htpasswd)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update htpasswd files through shell commands when the agent is allowed to run the bundled script.]

## Skill Version(s):

3.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
