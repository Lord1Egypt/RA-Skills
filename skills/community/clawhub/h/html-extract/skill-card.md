## Description:

HTML Extract helps agents convert local or remote HTML content into clean, structured Markdown using MinerU while preserving headings, lists, tables, and text hierarchy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract content from HTML files or web pages and convert it into clean Markdown for documentation, scraping, or downstream analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML files or URLs may be sent through MinerU's external service workflow.

Mitigation: Do not process private, proprietary, credential-bearing, or internal HTML unless external processing is intentional and approved.

Risk: The skill depends on a token-authenticated CLI installation.

Mitigation: Install mineru-open-api only from trusted sources, prefer pinned or isolated installs, and protect MINERU_TOKEN in local environments and logs.

## Reference(s):

- [HTML Extract ClawHub release](https://clawhub.ai/mzlzyca/skills/html-extract)
- [MinerU homepage](https://mineru.net)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU project](https://github.com/opendatalab/MinerU)
- [mineru-open-api Go package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The MinerU CLI can emit document content to stdout or write results to an output directory; progress and status messages are reported separately.]

## Skill Version(s):

0.4.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
