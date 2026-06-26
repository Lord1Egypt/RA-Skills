## Description: <br>
Open Exchange Rates provides exchange-rate data retrieval, currency listing, historical and time-series lookups, and conversions through the OOMOL connector instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Open Exchange Rates currency data, including latest rates, historical rates, time-series rates, supported currencies, and currency conversions through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires account credentials through the OOMOL connection flow. <br>
Mitigation: Use the OOMOL-connected account flow described by the skill; do not expose raw Open Exchange Rates API tokens to the agent. <br>
Risk: Connector inputs can change over time or differ by action. <br>
Mitigation: Inspect the live connector schema before each action and construct payloads only from that schema. <br>
Risk: Authentication, connection, or billing failures can interrupt requests. <br>
Mitigation: Run setup, reconnect, or billing recovery steps only when the corresponding command failure occurs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-open-exchange-rates) <br>
- [Open Exchange Rates homepage](https://openexchangerates.org) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill inspects the live connector schema before constructing action payloads and returns connector data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
