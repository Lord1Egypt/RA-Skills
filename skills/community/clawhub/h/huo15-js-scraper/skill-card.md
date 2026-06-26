## Description: <br>
JavaScript-rendered website scraping tool for pages such as WeCom documentation, Vue or React single-page apps, and sites where ordinary curl, wget, or web fetch tools cannot retrieve the rendered content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve rendered page text, structured JSON, and documentation content from JavaScript-heavy websites. It is also used to prepare WeCom documentation knowledge-base files and to support Qichacha workflows where authorized access is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used against scraping targets where automated access may be restricted or inappropriate. <br>
Mitigation: Review the target site's terms and account permissions before use, and run it only on sites and accounts where automated access is authorized. <br>
Risk: Qichacha login cookies are stored in a local reusable cookie file. <br>
Mitigation: Treat ~/.cache/huo15-js-scraper/qichacha_cookies.json as a secret, avoid shared machines, and delete the file when the workflow is complete. <br>
Risk: Anti-bot evasion behavior and rendered-page scraping can create account, compliance, or blocking risk. <br>
Mitigation: Prefer official APIs or MCP services when available, limit scraping volume, and review collected data before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-js-scraper) <br>
- [WeCom developer documentation](https://developer.work.weixin.qq.com) <br>
- [Qichacha MCP service](https://agent.qcc.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text, JSON, Markdown files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scraped content may depend on target-site authorization, login state, JavaScript rendering time, and selected engine.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence; artifact frontmatter remains 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
