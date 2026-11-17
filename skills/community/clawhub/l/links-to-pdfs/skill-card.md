## Description:

Scrapes documents from Notion, DocSend, direct PDF links, and other web sources into local PDF files, including authenticated sources through profiles and credential prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisling-dev](https://clawhub.ai/user/chrisling-dev)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill to download, archive, or convert web-hosted documents into local PDFs. It is especially relevant for direct PDFs, Notion pages, DocSend links, and authenticated document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and trust an unverified global docs-scraper CLI package.

Mitigation: Install only after reviewing and trusting the docs-scraper npm package and its publisher.

Risk: Authentication workflows can handle credentials and persisted browser sessions.

Mitigation: Avoid passing real passwords in command-line arguments, use the minimum required credentials, and clear saved profiles when finished.

Risk: Downloaded PDFs may contain sensitive information and are stored locally.

Mitigation: Treat files under ~/.docs-scraper/output as sensitive and run cleanup when the files are no longer needed.

Risk: The LLM fallback may send page HTML from private or authenticated pages to Claude.

Mitigation: Use the LLM fallback only when the page content can be shared with Claude and avoid it for private pages unless explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrisling-dev/skills/links-to-pdfs)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, local file paths, job IDs, and required credential types]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful scrapes return local PDF paths under ~/.docs-scraper/output; blocked scrapes return a job ID and required credential types.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
