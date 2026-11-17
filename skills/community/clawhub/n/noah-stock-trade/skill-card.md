## Description:

Noah Stock Trade helps agents query Noah securities account, holdings, asset, cash-flow, order, execution, fee-estimate, and buying-power information through the bundled read-only CLI while treating live order placement, modification, and cancellation as unsupported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyun9160-lgtm](https://clawhub.ai/user/xuyun9160-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Noah securities account, holdings, asset, cash-flow, order, execution, order-fee, and pre-trade fee or buying-power summaries. It is intended for read-only queries and pre-trade evaluation, not investment advice or live order execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens are required for account and trade queries, and the security review flags token handling as a serious concern.

Mitigation: Use a least-privilege read-only token, store secrets only in a user-owned protected location or environment, and avoid shared or untrusted workspaces.

Risk: The configured API destination is not allowlisted by the skill, so an unexpected base URL could receive authenticated requests.

Mitigation: Verify NOAH_TRADE_API_BASE_URL is HTTPS and the expected Noah API host before each run; add destination allowlisting before broader deployment.

Risk: The skill operates in a financial trading context where incorrect interpretation can affect account or order decisions.

Mitigation: Keep the skill to read-only queries and pre-trade evaluation, require human review for results, and do not enable live order placement, modification, or cancellation without explicit confirmation controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuyun9160-lgtm/skills/noah-stock-trade)
- [Publisher profile](https://clawhub.ai/user/xuyun9160-lgtm)
- [References index](references/README.md)
- [Auth and preflight](references/auth-and-preflight.md)
- [Current availability](references/current-availability.md)
- [Usage guide](references/usage-guide.md)
- [Output policy](references/output-policy.md)
- [Order status mapping](references/order-status-mapping.md)
- [Error catalog](references/error-catalog.md)
- [OpenAPI reference](references/openapi.yaml)
- [Noah trade API host](https://stock-open-api.noahgroup.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and concise human-facing text with optional CLI commands and structured summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should avoid dumping raw JSON, explain empty or failed results clearly, preserve read-only posture, and avoid cross-currency asset totals unless the API supplies an exchange-rate basis.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
