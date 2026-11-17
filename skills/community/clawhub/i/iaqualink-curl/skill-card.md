## Description:

Read iAqualink pool and chlorinator status from a shell using curl, including sign-in, system listing, and iAqua or eXO reads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and pool owners can use the shell commands to check iAqualink system status or troubleshoot API reads. Credentials are read from the macOS Keychain by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can issue pool-equipment changes, including toggle commands that can reverse the current state.

Mitigation: Treat installation as control-capable; use read-restricted access for status work, and require explicit approval plus a fresh state check before equipment changes.

Risk: Debug output may expose authentication tokens, and mishandled passwords can be exposed during sign-in.

Mitigation: Keep debug output private; redact tokens and keep passwords out of command arguments.

Risk: The cached session contains credentials, and eXO shadow behavior is unverified.

Mitigation: Protect the session file as a credential and verify eXO reads before relying on their output.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chrischall/skills/iaqualink-curl)
- [iaqualink.sh helper](references/iaqualink.sh)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell-command examples with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may return pool status and account-related data.]

## Skill Version(s):

0.3.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
