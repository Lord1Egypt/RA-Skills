## Description: <br>
Use markdown.new URLs to fetch readable web pages and convert them into static, structured Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctxinf](https://clawhub.ai/user/ctxinf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve public web pages, documentation, READMEs, blog posts, changelogs, and similar readable pages as Markdown for summarization, extraction, and downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private intranet URLs, authenticated pages, signed links, or URLs containing tokens may expose confidential content or credentials to markdown.new. <br>
Mitigation: Use this skill for public pages unless the user accepts sending the URL and reachable content to markdown.new; remove tokens, secrets, and confidential query parameters before use. <br>
Risk: HTTP errors, timeouts, blocked content, or heavily dynamic pages can produce failed or incomplete Markdown retrieval. <br>
Mitigation: Check for conversion failures and fall back to another access method when markdown.new does not return usable Markdown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ctxinf/markdown-new-skill) <br>
- [markdown.new URL pattern](https://markdown.new/{target_url}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The markdown.new service returns static, structured Markdown for readable public pages; agents should fall back to another retrieval method if conversion fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
