## Description:

Memory Hub helps agents synchronize shared memory in a private Git repository with read, write, sync, search, and merge operations for preference, knowledge, rule, and tool notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dr23334444](https://clawhub.ai/user/dr23334444)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Memory Hub to install and operate a shared-memory workflow across agents. The skill guides agents to synchronize concise preference, knowledge, rule, and tool notes through a private repository and local cache.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable shared repository content can persistently influence future agent behavior.

Mitigation: Use only a private, tightly controlled repository, inspect every change before syncing, and avoid loading RULES.md or TOOLS.md as authoritative instructions.

Risk: Shared memory may contain sensitive personal or credential data.

Mitigation: Do not store sensitive personal data, secrets, credentials, or access tokens in shared memory files.

Risk: The installer has an unsafe code path identified by the security evidence.

Mitigation: Do not run the installer until the Python interpolation bug is fixed and the script has been reviewed.

## Reference(s):

- [Upgrade Guide](references/upgrade-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can lead agents to read or update shared memory files, a local cache, and installation configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
