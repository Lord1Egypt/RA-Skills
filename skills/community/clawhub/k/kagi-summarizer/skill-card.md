## Description:

Summarizes URLs or text with Kagi's Universal Summarizer API, supporting configurable engines, prose or bullet takeaways, JSON output, and translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelazar](https://clawhub.ai/user/joelazar)

### License/Terms of Use:


## Use Case:

Developers, researchers, and other external users use this skill to summarize URLs, documents, papers, videos, or pasted text through Kagi. It is useful when an agent needs concise prose, bullet takeaways, translated summaries, or JSON output from a single supplied source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can download and run a mutable GitHub release binary without verification.

Mitigation: Prefer building from the included Go source, or verify any downloaded binary and checksum from a trusted release before execution.

Risk: Submitted URLs, documents, pasted text, or secrets may be sent to Kagi for summarization.

Mitigation: Use only data approved for Kagi processing, and avoid confidential documents, internal URLs, secrets, or regulated data unless Kagi use is approved for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joelazar/skills/kagi-summarizer)
- [Kagi Universal Summarizer API](https://help.kagi.com/kagi/api/summarizer.html)
- [Kagi API Portal](https://kagi.com/settings/api)
- [Kagi API Billing and Pricing](https://kagi.com/settings/billing_api)
- [Kagi Skills GitHub Releases](https://github.com/joelazar/kagi-skills/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Plain text summaries or structured JSON, with Markdown setup and usage guidance containing shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KAGI_API_KEY; token usage and API balance may be written to stderr.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
