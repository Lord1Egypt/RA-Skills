## Description: <br>
WebScraper.io (webscraper.io). Use this skill for reading, creating, updating, and deleting WebScraper.io data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect WebScraper.io schemas and run Web Scraper Cloud actions through an OOMOL-connected account, including sitemap and scraping job management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run account-changing WebScraper.io operations, including creating jobs, updating sitemaps, exporting data, and deleting items. <br>
Mitigation: Confirm the exact action, target, and payload with the user before write or destructive operations, and inspect the live action schema before constructing payloads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-webscraper-io) <br>
- [WebScraper.io Homepage](https://webscraper.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include connector response JSON containing data and meta.executionId when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
