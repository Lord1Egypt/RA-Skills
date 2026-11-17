## Description:

Scrape web pages privately with encrypted local storage, optional PII removal, and secure memory-only retrieval - featuring explicit zero-local-data-retention mode and verifiable memory wiping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-hussein](https://clawhub.ai/user/z-hussein)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy-conscious users use this skill to request web-page scraping, configure retention and PII-removal options, and retrieve saved results. Review its implementation and retention behavior before using it with sensitive information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented privacy guarantees may conflict with the described behavior, and excerpts are saved by default.

Mitigation: Review the implementation and actual retention behavior before sensitive use; inspect excerpts for personal or confidential information before sharing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/z-hussein/skills/privacy-scraper)
- [OpenClaw documentation](https://docs.openclaw.ai/)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Text, Files, Configuration instructions]

**Output Format:** [Shell command invocations, Markdown excerpts, and scrape or retrieval results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scraping may create an encrypted vault file and, when enabled, an excerpt; retrieval returns decrypted text.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
