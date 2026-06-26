## Description: <br>
Enables agents to search eBay products, retrieve product details, get autocomplete suggestions, and check Countdown API account status through the OOMOL `countdown_api` connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to access Countdown API data through an installed and connected OOMOL account. It supports product search, product detail retrieval, autocomplete, and account usage checks while instructing agents to inspect live action schemas before connector calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected OOMOL account with Countdown API credentials. <br>
Mitigation: Install only for users who intend to use the Countdown API connector, and resolve authentication or connection errors through the documented first-time setup steps. <br>
Risk: Connector action inputs can change with the live Countdown API contract. <br>
Mitigation: Inspect the action schema before constructing each payload and confirm any write or destructive action with the user before execution. <br>


## Reference(s): <br>
- [Countdown API homepage](https://countdownapi.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill listing](https://clawhub.ai/oomol/oo-countdown-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include a data object and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
