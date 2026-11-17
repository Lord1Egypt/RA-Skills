## Description:

OpenClaw skill for source-backed web search, page reading, and evidence-aware claim checking, with no API keys required by default and optional providers for stronger coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run live web searches, browse source pages, verify concrete claims, and produce citation-ready evidence summaries. It is intended for factual, recent, or source-sensitive work where results should include URLs and support or conflict signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned external package whose executable code was not included for review.

Mitigation: Install only in an isolated virtual environment, avoid installing as root, and prefer a pinned, hash-verified package version after reviewing the package source.

Risk: Optional Bright Data or other provider credentials may cause providers to receive the relevant queries and URLs.

Mitigation: Enable optional providers only when approved for the use case, and provide credentials only when sharing those queries and URLs with the provider is acceptable.

Risk: The documented claim verification is heuristic and may not resolve conflicting sources.

Mitigation: Treat verification scores as decision support, review cited sources directly, and preserve surfaced conflicts in downstream answers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wd041216-bit/skills/openclaw-free-web-search)
- [Project Homepage](https://github.com/wd041216-bit/zero-api-key-web-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-capable command output with source URLs, verification scores, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include support and conflict classifications, page-aware verification status, provider setup guidance, and citation-ready URLs.]

## Skill Version(s):

23.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
