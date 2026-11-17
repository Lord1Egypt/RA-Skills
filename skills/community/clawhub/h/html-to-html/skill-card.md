## Description:

HTML to HTML helps agents clean and restructure remote or local HTML into clean, structured HTML using MinerU while preserving core content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content migration teams, and automation agents use this skill to convert cluttered web pages, CMS exports, scraped pages, or local HTML files into cleaner structured HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pages, local HTML files, and extracted content may contain confidential, regulated, proprietary, or internal-only information before they are submitted to MinerU's external service.

Mitigation: Use the skill only for content approved for MinerU processing, and avoid sending sensitive HTML unless organizational policy permits it.

Risk: MINERU_TOKEN is sensitive credential material that could be exposed through logs, shell history, or source control.

Mitigation: Keep MINERU_TOKEN out of logs and repositories, prefer environment-variable or interactive authentication, and rotate the token if exposure is suspected.

Risk: Installing mineru-open-api globally or from an unpinned source can increase supply-chain or environment-change risk.

Mitigation: Prefer pinned or isolated installation of mineru-open-api when practical, and review installation commands before execution.

## Reference(s):

- [HTML to HTML on ClawHub](https://clawhub.ai/mzlzyca/skills/html-to-html)
- [MinerU](https://mineru.net)
- [MinerU API token management](https://mineru.net/apiManage/token)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, HTML]

**Output Format:** [Markdown guidance with inline shell commands and clean HTML output from MinerU.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mineru-open-api and MINERU_TOKEN; remote crawl and local extract commands can write output to stdout or a selected directory.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
