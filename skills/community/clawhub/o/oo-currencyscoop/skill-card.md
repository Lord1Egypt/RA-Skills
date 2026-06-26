## Description: <br>
CurrencyBeacon (currencybeacon.com) helps agents search and read CurrencyBeacon exchange-rate data through the OOMOL currencyscoop connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert currencies, list supported currencies, and retrieve latest, historical, or time-series exchange rates through an OOMOL-connected CurrencyBeacon account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a suspicious provider-identity mismatch: CurrencyBeacon branding conflicts with the CurrencyScoop connector and credential setup path. <br>
Mitigation: Confirm with OOMOL whether this release is intended to use CurrencyBeacon or CurrencyScoop before connecting credentials, and do not enter API credentials until the provider identity is clarified. <br>
Risk: The skill may ask the agent to install or use an external oo CLI before running connector actions. <br>
Mitigation: Use an already trusted oo CLI installation where possible, and avoid running the external installer unless the OOMOL install path is trusted. <br>


## Reference(s): <br>
- [CurrencyBeacon homepage](https://currencybeacon.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-currencyscoop) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, an authenticated OOMOL account, and a connected CurrencyBeacon or currencyscoop provider credential.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
