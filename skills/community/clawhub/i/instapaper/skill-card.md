## Description:

Use when operating the instapaper-cli (ip) tool or troubleshooting it: authenticating, listing/exporting/importing bookmarks, bulk mutations, folders/highlights/text, choosing output formats (ndjson/json/plain), cursor-based sync, and interpreting stderr-json/exit codes for automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vburojevic](https://clawhub.ai/user/vburojevic)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to operate and troubleshoot the Instapaper CLI with reliable authentication, bookmark sync, import/export, bulk mutation, folders, highlights, article text retrieval, structured output, and error handling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI without pinning or verification can introduce supply-chain uncertainty.

Mitigation: Pin and verify the Instapaper CLI version before installing when possible.

Risk: Authentication examples can expose credentials if users paste real passwords directly into shell commands.

Mitigation: Use an interactive prompt, protected secret manager, or another method that avoids shell history and logs.

Risk: Delete, folder delete, import, and bulk mutation commands can make destructive or large-scale account changes.

Mitigation: Review destructive commands before execution and use dry-run, idempotent, batch, and explicit confirmation options where supported.

## Reference(s):

- [Commands](references/commands.md)
- [Errors and exit codes](references/errors.md)
- [Output, progress, and sync](references/output-and-sync.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON/NDJSON output-format guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may guide use of structured stderr JSON, progress JSON, cursor files, dry runs, and explicit confirmation flags for destructive operations.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
