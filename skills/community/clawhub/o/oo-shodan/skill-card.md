## Description: <br>
Shodan (shodan.io). Use this skill for Shodan requests that search and read internet-exposure data through the OOMOL Shodan connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and operators use this skill to query Shodan host data, DNS information, subdomains, facets, and account credit information from an OOMOL-connected Shodan account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Shodan account and sensitive credentials managed through OOMOL. <br>
Mitigation: Use only with the intended OOMOL account connection, avoid handling raw tokens, and perform setup only after an auth or connection failure. <br>
Risk: Incorrect Shodan queries can return irrelevant or misleading exposure data. <br>
Mitigation: Inspect the live connector action schema before building payloads and review query terms, facets, and target identifiers before execution. <br>
Risk: Account credit or billing limits can stop Shodan actions. <br>
Mitigation: Check account API information or billing status when the connector reports insufficient credit before retrying. <br>


## Reference(s): <br>
- [Shodan homepage](https://www.shodan.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-shodan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include JSON data and execution metadata from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
