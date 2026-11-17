## Description:

Provides MCP-native guidance, recipes, and helper scripts for using Scrapling to fetch pages, extract data, crawl sites, and handle anti-bot workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute authorized web scraping through Scrapling MCP calls and helper scripts, including static fetches, browser-rendered pages, selector extraction, and spider-style crawls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad network scraping, anti-bot handling, proxy workflows, and login-capable browser automation.

Mitigation: Run it only for targets the user is authorized to scrape, require URL or domain allowlists, and avoid stealth, proxy, or login modes unless permission is explicit.

Risk: Automated MCP or helper-script execution can make outbound requests beyond the intended scope.

Mitigation: Install and run in an isolated unprivileged environment with outbound network controls, private-network blocking, rate limits, and manual approval for new target domains.

Risk: Scraping scripts and spider recipes may create local output or checkpoint files.

Mitigation: Run from a workspace-limited directory, review script arguments before execution, and inspect generated files before sharing or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/nidhov01-scrapling-web-scraping)
- [Scrapling MCP setup](artifact/references/mcp-setup.md)
- [Anti-bot handling](artifact/references/anti-bot.md)
- [Proxy rotation](artifact/references/proxy-rotation.md)
- [Spider recipes](artifact/references/spider-recipes.md)
- [Scrapling quick reference](artifact/references/api_reference.md)
- [Scrapling documentation](https://scrapling.readthedocs.io)
- [Scrapling GitHub repository](https://github.com/D4Vinci/Scrapling)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON snippets, Python examples, shell commands, and JSON command output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts can make outbound network requests and may write local output files when scraping or spider recipes are run.]

## Skill Version(s):

0.4.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
