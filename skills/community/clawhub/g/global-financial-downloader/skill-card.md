## Description:

Global Financial Downloader helps agents download annual, interim, quarterly, and SEC-style financial reports for A-share, Hong Kong, and US stocks using stock codes or mapped company names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent operators use this skill to select market-aware downloader parameters and run a Python CLI that retrieves company financial disclosure files across supported global markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted report-type input can be interpreted as shell commands and run arbitrary local commands.

Mitigation: Use only trusted, fixed report-type values, avoid passing free-form input, and prefer --dry-run until command construction is changed to argument-list subprocess calls with strict report-type allowlisting.

Risk: The downloader contacts external financial disclosure sources and stores downloaded files in the OpenClaw workspace.

Mitigation: Run it in a controlled workspace, review stock identifiers and year ranges before execution, and confirm network and data-handling policies before downloading reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/skills/global-financial-downloader)
- [Publisher profile](https://clawhub.ai/user/cgxxxxxxxxxxxx)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash examples; downloader runs produce JSON, CSV, and optional PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and writes downloaded reports into the OpenClaw workspace export or archive directories.]

## Skill Version(s):

2.3.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
