## Description: <br>
HasData lets agents fetch real-time web data through the hasdata CLI, including search, news, shopping, maps, real estate, jobs, reviews, and arbitrary URL scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hasdata](https://clawhub.ai/user/hasdata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to ground responses with current web data, gather structured data from public services, and scrape user-specified URLs through the HasData CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad web scraping and enrichment workflows that can expose privacy, authorization, or targeting concerns. <br>
Mitigation: Use it only for authorized data collection, avoid private-person profiling or unsolicited targeting, and prefer SERP-based public snippets before escalating to direct page scraping. <br>
Risk: The skill depends on an external CLI installer and a sensitive HasData API key stored in the user environment. <br>
Mitigation: Review the installer before execution, configure only a user-provided API key, and protect ~/.hasdata/config.yaml as a credential-bearing file. <br>
Risk: Passing session cookies or custom headers to scraping commands can access account-scoped data. <br>
Mitigation: Only pass cookies or authenticated headers when explicitly authorized by the account owner and required for the task. <br>


## Reference(s): <br>
- [HasData skill page](https://clawhub.ai/hasdata/hasdata-api) <br>
- [HasData CLI](https://github.com/HasData/hasdata-cli) <br>
- [HasData website](https://hasdata.com) <br>
- [Data enrichment reference](artifact/references/enrichment.md) <br>
- [Search reference](artifact/references/search.md) <br>
- [Web scraping reference](artifact/references/web-scraping.md) <br>
- [Real estate reference](artifact/references/real-estate.md) <br>
- [E-commerce reference](artifact/references/ecommerce.md) <br>
- [Local business reference](artifact/references/local-business.md) <br>
- [Jobs reference](artifact/references/jobs.md) <br>
- [All commands reference](artifact/references/all-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-processing examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the hasdata CLI and a user-provided HasData API key; CLI responses are typically JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
