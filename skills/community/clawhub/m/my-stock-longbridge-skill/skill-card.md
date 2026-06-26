## Description: <br>
Integrates Longbridge OpenAPI for stock trading, market data, account and position tracking, and order notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators can use this skill to manage Longbridge stock-trading workflows, including order submission, cancellation, quote access, account review, and private order-status notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded Longbridge brokerage credentials are present in the artifact. <br>
Mitigation: Rotate the exposed credentials, remove hardcoded tokens, and require credentials to be supplied through a secret store before installation. <br>
Risk: The skill can submit or cancel preset brokerage orders. <br>
Mitigation: Require explicit user confirmation or dry-run mode before every order action, with symbol, side, quantity, order type, and price visible before execution. <br>
Risk: Private order details can be forwarded to a fixed notification recipient. <br>
Mitigation: Make notification recipients configurable and opt-in, and avoid sending account-linked trade details unless the user has approved the destination. <br>
Risk: Dependencies are not version-pinned. <br>
Mitigation: Pin dependency versions and re-scan the resolved environment before reconsidering installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canonxu/my-stock-longbridge-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/canonxu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Text and Markdown with Python code references, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger brokerage API calls and local order-history file updates when executed in an installed environment.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; SKILL.md frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
