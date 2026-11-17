## Description:

Convert HTML files and URLs to PDF using Puppeteer with options for margins, page size, orientation, headers, and footers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hankagent](https://clawhub.ai/user/hankagent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert local HTML documents, web pages, and reports into PDF files with configurable print options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL conversion can fetch arbitrary network targets from the user's machine.

Mitigation: Use only trusted local HTML or trusted public URLs, and avoid internal, private, link-local, or metadata service URLs.

Risk: PDF output paths are user-selected and could overwrite important files if chosen carelessly.

Mitigation: Choose output paths deliberately and write PDFs into a controlled working directory.

Risk: Browser installation or execution can add supply-chain and runtime exposure.

Mitigation: Pin Puppeteer with a lockfile, run conversion in a container or network-restricted environment, and only use verified browser binaries.

## Reference(s):

- [API Reference](references/api.md)
- [Setup & Requirements](references/setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of a Puppeteer script that writes PDF files to user-selected output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
