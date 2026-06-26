## Description: <br>
Firecrawl helps agents use an OOMOL-connected Firecrawl account to scrape, crawl, search, map URLs, extract structured data, and manage related jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Firecrawl scraping, crawling, search, extraction, mapping, usage, queue, and job-management actions through the oo CLI. It is intended for Firecrawl workflows where the agent should inspect each live action schema before submitting JSON payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends submitted URLs and extraction inputs to OOMOL and Firecrawl using connected account credentials. <br>
Mitigation: Confirm the user trusts OOMOL and Firecrawl with the URLs and data before installing or running the skill. <br>
Risk: Crawl, batch, agent, and research jobs can consume account credits or tokens. <br>
Mitigation: Review job scope and monitor credit, token, queue, and billing status before starting large or long-running jobs. <br>
Risk: Write, cancel, or destructive actions can change Firecrawl job state. <br>
Mitigation: Require explicit user approval for the exact target and payload before running actions tagged as write or destructive. <br>


## Reference(s): <br>
- [ClawHub Firecrawl listing](https://clawhub.ai/oomol/oo-firecrawl) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Firecrawl homepage](https://www.firecrawl.dev) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Firecrawl action results returned as JSON through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
