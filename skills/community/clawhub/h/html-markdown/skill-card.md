## Description:

Converts local HTML files and web pages to clean Markdown using MinerU while preserving common document structure such as headings, lists, tables, links, and code blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content teams use this skill to convert HTML pages or files into Markdown for documentation, content migration, and Markdown-based publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted HTML files or URLs may be processed by MinerU's cloud/API service, which can expose sensitive page content if submitted without approval.

Mitigation: Treat converted HTML and URLs as potentially sent to MinerU's service, and do not submit sensitive internal pages unless that is approved.

Risk: Installing the MinerU CLI from an untrusted or floating source can introduce supply-chain risk.

Mitigation: Install only from a trusted MinerU source and prefer a pinned version or isolated environment.

Risk: A MinerU token is required for HTML conversion and could be exposed in shared environments.

Mitigation: Use a limited MinerU token and keep authentication in the MINERU_TOKEN environment variable or MinerU auth flow rather than in skill text or committed files.

## Reference(s):

- [MinerU homepage](https://mineru.net)
- [MinerU API token management](https://mineru.net/apiManage/token)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU Open API Go package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated Markdown output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTML conversion requires MinerU authentication; progress and status messages are sent to stderr while document content is sent to stdout.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
