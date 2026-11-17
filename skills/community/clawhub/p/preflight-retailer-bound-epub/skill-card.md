## Description:

Preflights the exact retailer-bound .epub build for automated EPUB 2/3 specification failures before upload, handoff, rejection repair, or regression checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powmcp](https://clawhub.ai/user/powmcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, publishing teams, and ebook production staff use this skill to run an automated EPUB 2/3 specification preflight on the exact retailer-bound EPUB bytes and to guide repairs from returned EPUBCheck findings. It does not cover accessibility, reading-system rendering, editorial quality, or retailer-specific metadata acceptance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path is unpinned, so installation may resolve to code or package contents that differ from the reviewed release.

Mitigation: Prefer a pinned installer or reviewed commit before deployment, and confirm the installed source matches the reviewed release evidence.

Risk: EPUB bytes or direct public EPUB URLs are sent to a third-party MCP service for checking.

Mitigation: Use this skill only when PowMCP is trusted with the EPUB content or URL, and avoid authenticated URLs, credentials, secrets, and query-string tokens.

Risk: Running setup from a credentialed environment may expose unrelated confidential files or production credentials if the installer or tool behavior changes.

Mitigation: Run setup and checks from an environment without production credentials or unrelated confidential files.

## Reference(s):

- [Ebook File Check reference](references/epub-check.md)
- [ClawHub skill page](https://clawhub.ai/powmcp/skills/preflight-retailer-bound-epub)
- [Publisher profile](https://clawhub.ai/user/powmcp)
- [Ebook File Check app](https://powmcp.com/apps/epub-check/)
- [W3C EPUBCheck](https://www.w3.org/publishing/epubcheck)
- [Official EPUBCheck implementation](https://github.com/w3c/epubcheck)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and structured EPUB preflight report sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include EPUBCheck pass or fail state, EPUB version, severity counts, finding locations, SHA-256, structural inventory, truncation status, repair guidance, and comparison summaries when the PowMCP MCP tool returns them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
