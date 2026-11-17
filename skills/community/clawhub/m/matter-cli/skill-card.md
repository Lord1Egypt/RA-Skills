## Description:

Interact with a user's Matter reading library using the Matter CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicholope](https://clawhub.ai/user/nicholope)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to browse, search, save, tag, archive, summarize, and track progress in a Matter reading library through the Matter CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow downloads a mutable Matter CLI binary from the latest GitHub release.

Mitigation: Review the install command before use and prefer a pinned Matter CLI release with a verified checksum or signature.

Risk: Authenticated Matter CLI commands can modify or delete library items, annotations, and tags.

Mitigation: Only use the skill when the user explicitly means their Matter account, and confirm destructive actions before execution.

Risk: Bulk operations can hit Matter rate limits and corrupt JSON output mid-stream when `--all` is used on large libraries.

Mitigation: Use manual cursor pagination with delays, and stop immediately when a rate-limit retry message is returned.

## Reference(s):

- [Matter CLI command reference](references/commands.md)
- [Matter CLI GitHub repository](https://github.com/getmatterapp/matter-cli)
- [Matter CLI skill page](https://clawhub.ai/nicholope/skills/matter-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; Matter CLI command responses are JSON by default with an optional plain-text mode.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use cursor-based pagination and deliberate sleeps to respect Matter CLI rate limits.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
