## Description: <br>
Jin10 helps agents search and read Jin10 market quotes, economic calendar items, flash news, and news articles through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to retrieve Jin10 financial market data and news through the oo CLI after the user has connected a Jin10 account in OOMOL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Jin10 account and may consume account access or credits. <br>
Mitigation: Install and use it only when Jin10 access through OOMOL is intended, and review connection status and billing before repeated queries. <br>
Risk: First-time setup may require installing or authenticating the oo CLI. <br>
Mitigation: Review the OOMOL CLI installer and authentication flow before setup, and only run setup commands when the connector fails for installation, authentication, or connection reasons. <br>


## Reference(s): <br>
- [Jin10 homepage](https://www.jin10.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-jin10) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads or responses from oo CLI actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Jin10 connector actions return structured data and an execution ID when run with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
