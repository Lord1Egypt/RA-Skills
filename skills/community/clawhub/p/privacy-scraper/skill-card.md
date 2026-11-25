## Description:

Scrapes web pages, stores full results in an encrypted local vault, optionally creates a PII-filtered excerpt, and retrieves saved content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-hussein](https://clawhub.ai/user/z-hussein)

### License/Terms of Use:

MIT

## Use Case:

Developers and privacy-conscious users can scrape public web pages, keep full results in an encrypted local vault, optionally produce a PII-filtered excerpt, and retrieve saved results for later use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial because four local path references were unresolved, so the benign verdict has medium confidence.

Mitigation: Review the unresolved references before installation and consider the incomplete scan evidence when deciding whether to install.

Risk: PII removal is best-effort, so an excerpt may retain identifiers or confidential content.

Mitigation: Inspect excerpts for residual identifiers and confidential information before sharing.

Risk: Retrieved plaintext may persist in host swap, crash dumps, or stdout capture buffers.

Mitigation: Avoid capturing retrieval output and use host settings that limit swap and crash-dump exposure when handling sensitive content.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai/)
- [Privacy Scraper release page](https://clawhub.ai/z-hussein/skills/privacy-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Scrape result data, optional Markdown excerpts, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each scrape creates an encrypted vault file; an excerpt is optional, and retrieval returns decrypted text to the caller.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
