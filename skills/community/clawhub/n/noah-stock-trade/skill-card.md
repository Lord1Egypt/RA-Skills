## Description: <br>
Noah Stock Trade helps agents query stock trading account information, holdings, securities assets, capital flows, orders, deals, order details, fee details, pre-trade fee estimates, and buy/sell availability while keeping live order placement, modification, and cancellation out of scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyun9160-lgtm](https://clawhub.ai/user/xuyun9160-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route stock account, portfolio, order, deal, fee, and pre-trade availability questions through a controlled CLI workflow. It is suited to read-only trading-account queries and pre-trade evaluation, not live order submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive stock account, holdings, order, asset, deal, and capital-flow data through a user-provided trading API token. <br>
Mitigation: Install only from a trusted publisher, prefer a read-only or test token when available, and keep the token out of the skill files. <br>
Risk: Using an incorrect API base URL or token scope could expose data to the wrong environment or cause failed account queries. <br>
Mitigation: Confirm the configured trading API base URL and Bearer token permissions before use. <br>
Risk: Users may interpret pre-trade estimates or availability checks as approval to place real trades. <br>
Mitigation: Treat outputs as read-only query or pre-trade evaluation results, and do not use this version for placing, modifying, or canceling trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyun9160-lgtm/noah-stock-trade) <br>
- [Skill definition](SKILL.md) <br>
- [Current Availability](references/current-availability.md) <br>
- [Auth and Preflight](references/auth-and-preflight.md) <br>
- [Usage Guide](references/usage-guide.md) <br>
- [Output Policy](references/output-policy.md) <br>
- [API Issues / Follow-ups](references/api-issues.md) <br>
- [Order Status Mapping](references/order-status-mapping.md) <br>
- [OpenAPI reference](references/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text, JSON] <br>
**Output Format:** [Concise user-facing text or Markdown, with structured JSON available from the CLI wrappers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-provided Bearer token and configured trading API base URL; live order placement, modification, and cancellation are not exposed in this release.] <br>

## Skill Version(s): <br>
0.1.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
