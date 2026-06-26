## Description: <br>
ScrapingBee (scrapingbee.com). Use this skill for ANY ScrapingBee request -- searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch HTML, extract structured JSON from public web pages, and retrieve ScrapingBee usage statistics through an OOMOL-connected ScrapingBee account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL/ScrapingBee account and routes requested URLs and extracted page data through an external connector service. <br>
Mitigation: Install and use it only when the user trusts OOMOL's oo CLI and accepts that ScrapingBee requests and extracted page data are processed by the connected service. <br>
Risk: First-time setup may require running an oo CLI install command and signing in. <br>
Mitigation: Review installation commands before execution and only run setup steps after an auth, connection, or missing-command failure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-scrapingbee) <br>
- [ScrapingBee Homepage](https://www.scrapingbee.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include external connector responses containing HTML, structured JSON extraction results, usage statistics, or setup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
