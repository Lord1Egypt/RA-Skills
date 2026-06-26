## Description: <br>
Comprehensive CLI for Krónan.is grocery shopping through the official Public API, supporting product search, categories, carts, orders, product lists, purchase statistics, and shopping notes for humans and AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arnif](https://clawhub.ai/user/arnif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents with a Krónan account use this skill to run kronan-cli commands for grocery discovery, cart and order management, product lists, shopping notes, and purchase-statistics review. Agents should request explicit confirmation before commands that change real account data. <br>

### Deployment Geography for Use: <br>
Iceland <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real grocery-account state, including carts, orders, lists, notes, and purchase-stat visibility. <br>
Mitigation: Require explicit user approval before running state-changing commands and review command arguments before execution. <br>
Risk: The Krónan API token is a credential stored at ~/.kronan/token. <br>
Mitigation: Treat the token like a password, restrict local file permissions, and revoke it from the Krónan account when no longer needed. <br>
Risk: Installation runs a repository script and downloads a release binary. <br>
Mitigation: Install only after trusting the GitHub repository, install script, and release binary. <br>
Risk: Identity and shopping activity commands can expose personal information. <br>
Mitigation: Avoid sharing command output that contains identity, order, cart, note, or purchase-history details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arnif/kronan) <br>
- [kronan-cli homepage](https://github.com/arnif/kronan-cli) <br>
- [Krónan Public API Swagger UI](https://api.kronan.is/api/v1/schema/swagger-ui/) <br>
- [Krónan Public API ReDoc](https://api.kronan.is/api/v1/schema/redoc/) <br>
- [Krónan access token settings](https://kronan.is/adgangur/adgangslyklar) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; CLI commands can return text or JSON with --json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally stored Krónan API access token for authenticated commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
