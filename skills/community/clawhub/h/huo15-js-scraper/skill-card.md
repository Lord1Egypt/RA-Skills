## Description:

JavaScript-rendered website scraping tool for pages such as WeCom documentation, Vue/React single-page apps, and Qichacha company data pages, with Playwright and scrapling engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to extract content from JavaScript-rendered web pages and to build local Markdown knowledge-base files from WeCom documentation. It also provides a Qichacha company-data fallback scraper when the official MCP/API route is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict marks the release suspicious because it asks users to load an unaudited external GitHub skill.

Mitigation: Do not load the external GitHub skill unless it has been separately trusted and reviewed.

Risk: The Qichacha direct-scraping path stores cookies locally as session credentials.

Mitigation: Protect the cookie file, restrict file permissions where possible, and delete it after use.

Risk: The skill recommends dependency installation commands that may affect the user's Python environment.

Mitigation: Install and run the skill in an isolated virtual environment and avoid --break-system-packages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-js-scraper)
- [WeCom developer documentation](https://developer.work.weixin.qq.com)
- [WeCom document example](https://developer.work.weixin.qq.com/document/path/91756)
- [Qichacha MCP service](https://agent.qcc.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scraper scripts emit plain text, JSON, or Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write scraped WeCom documentation under a local knowledge-base directory and may save Qichacha login cookies under the user's cache directory.]

## Skill Version(s):

1.2.2 (source: server release metadata; artifact frontmatter and _meta.json report 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
