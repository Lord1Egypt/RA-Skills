## Description:

Get India NSE stock market data via FinanceAgent on OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query India NSE stock market data through OneKey Gateway by providing one or more NSE stock symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned external npm gateway package.

Mitigation: Review the npm package before use, pin a reviewed version, and avoid global installation when possible.

Risk: The curl example uses verbose mode with an API key header, which can expose the key in logs or screenshots.

Mitigation: Remove verbose mode, keep the OneKey API key out of logs and screenshots, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/india-stock-market-nse-india)
- [DeepNLP OneKey Agent Router endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON]

**Output Format:** [Markdown guidance with shell and curl examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and a symbol_list array of NSE stock symbols.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
