## Description: <br>
Use currencyapi through the OOMOL-connected `oo` CLI to convert currencies, retrieve latest or historical exchange rates, list supported currencies, and check account quota status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate currencyapi through an OOMOL-connected account for currency conversion, exchange-rate lookup, supported-currency discovery, and account quota checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL account with currencyapi connected and may prompt first-time CLI installation or login when the local environment is not configured. <br>
Mitigation: Install only when currencyapi access through OOMOL is intended, and complete CLI login or provider connection only after an auth or connection error indicates it is required. <br>
Risk: currencyapi requests may be routed through OOMOL rather than direct API calls. <br>
Mitigation: Review the OOMOL-connected credential flow and organizational data-handling requirements before using the connector. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-currencyapi) <br>
- [currencyapi homepage](https://currencyapi.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON responses from the `oo connector run` workflow when executed with `--json`.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
