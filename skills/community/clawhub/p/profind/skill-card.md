## Description:

ProFind helps agents operate the macOS ProFind application for indexed file search, content and metadata queries, advanced filters, script hooks, URL-scheme launches, and local SOAP API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steve-shi-web](https://clawhub.ai/user/steve-shi-web)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to help an agent compose ProFind searches, open ProFind search windows, invoke script actions, and query the optional local Media Server interface. It is intended for file discovery, metadata/content lookup, and guided batch-operation workflows on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation helpers can access broad local file locations when ProFind has Full Disk Access.

Mitigation: Grant Full Disk Access only when protected locations must be searched, and scope searches to the narrowest practical paths.

Risk: Script hooks and sample batch operations can modify local files.

Mitigation: Review proposed scripts before use, add confirmations and dry-run previews for bulk changes, and check for filename collisions before renaming or moving files.

Risk: CLI and URL-scheme search text may be unsafe when populated from untrusted input.

Mitigation: Escape or validate search terms and avoid passing untrusted input to the included CLI or script examples until input handling is hardened.

Risk: The optional Media Server exposes ProFind search results through a local HTTP SOAP interface.

Mitigation: Keep Media Server disabled unless needed and review local access assumptions before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steve-shi-web/skills/profind)
- [Publisher profile](https://clawhub.ai/user/steve-shi-web)
- [ProFind on the App Store](https://apps.apple.com/app/id1559203395)
- [API reference](docs/API-REFERENCE.md)
- [URL scheme reference](docs/URL-SCHEME.md)
- [Sample scripts reference](docs/SAMPLE-SCRIPTS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, AppleScript, URL-scheme, and SOAP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may launch local macOS applications or propose scripts that act on selected files; users should review commands before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
