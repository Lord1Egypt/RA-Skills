## Description:

Mx Stock Simulator helps agents query and manage an A-share simulated stock portfolio, including positions, funds, orders, historical trades, buy/sell requests, and cancellations through an authenticated API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessecq1995](https://clawhub.ai/user/jessecq1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to practice A-share portfolio operations, check simulated holdings and balances, review orders and trades, and submit simulated buy, sell, or cancellation requests. It is not a source of investment advice and does not perform live-money trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an API key for account-like simulated trading APIs.

Mitigation: Use a low-privilege, revocable MX_APIKEY and keep it in environment configuration rather than exposing it in prompts, logs, or shared files.

Risk: The skill can submit buy, sell, and cancellation requests in a simulated portfolio.

Mitigation: Require explicit user confirmation before allowing an agent to execute buy, sell, or cancel requests.

Risk: The skill writes raw financial API responses to the local OpenClaw workspace output directory.

Mitigation: Periodically delete or protect files under /root/.openclaw/workspace/mx_data/output and avoid sharing those outputs unless reviewed.

Risk: Changing MX_API_URL could direct credentials and portfolio requests to an untrusted endpoint.

Mitigation: Keep MX_API_URL set to the documented trusted HTTPS host unless the endpoint has been independently approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jessecq1995/skills/mx-stock-simulator)
- [Publisher profile](https://clawhub.ai/user/jessecq1995)
- [Configured API base URL](https://mkapi2.dfcfs.com/finskillshub)
- [Miaoxiang account setup page](https://dl.dfcfs.com/m/itc4)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write raw JSON response files and extracted text files under the configured OpenClaw workspace output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
