## Description: <br>
Nmb Scrapling helps agents produce Scrapling-based web scraping guidance, code, shell commands, and configuration for static, dynamic, stealthy, and large-scale crawling workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Superowl](https://clawhub.ai/user/Superowl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill when they want an agent to explain or scaffold Scrapling workflows for scraping websites, extracting structured data, handling dynamic pages, managing sessions, monitoring changes, or setting up the Scrapling MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stealth mode, Cloudflare solving, proxy rotation, logged-in sessions, and large crawls can be misused or violate site rules. <br>
Mitigation: Use the skill only for websites you are authorized to scrape, make bypass and proxy features explicit opt-ins, respect robots.txt and site terms, and set clear scope and rate limits. <br>
Risk: Scraping workflows can collect sensitive or excessive data. <br>
Mitigation: Minimize collected fields, avoid credentials or personal data unless approved, and clean up crawl and session state when finished. <br>
Risk: Generated commands may install or execute the third-party Scrapling package and browser components. <br>
Mitigation: Review generated commands before execution and pin or verify Scrapling package versions where practical. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Superowl/nmb-scrapling) <br>
- [Scrapling documentation](https://scrapling.readthedocs.io) <br>
- [Scrapling GitHub repository](https://github.com/D4Vinci/Scrapling) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python, Bash, and JSON snippets; the bundled quick-scrape script can also produce JSON or text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on target URLs, CSS selectors, fetcher mode, output path, authorization scope, and rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
