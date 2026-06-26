## Description: <br>
한국투자증권(KIS) Open API를 이용한 국내 주식 트레이딩. 잔고 조회, 시세 확인, 매수/매도 주문, 매매 내역, 시장 개황 등. | Korean stock trading via KIS (Korea Investment & Securities) Open API. Balance, quotes, buy/sell orders, trade history, market overview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tgparkk](https://clawhub.ai/user/tgparkk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Korean stock account balances, holdings, quotes, order history, and market information through the KIS Open API. It can also prepare and submit KRX buy and sell orders when configured with brokerage credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit live KIS brokerage buy or sell orders, and the order script does not enforce an interactive confirmation before non-dry-run execution. <br>
Mitigation: Require explicit user approval before any non-dry-run order command, run order.py with --dry-run first, and verify symbol, side, quantity, price, and account mode before execution. <br>
Risk: The skill uses brokerage credentials and stores access tokens under ~/.kis-trading. <br>
Mitigation: Keep config.ini and token.json private, restrict file permissions, avoid sharing command output that exposes account details, and rotate credentials if local files are exposed. <br>
Risk: A misconfigured BASE_URL can direct orders to live trading instead of the mock trading endpoint. <br>
Mitigation: Start with the mock endpoint, verify BASE_URL before each trading session, and use the production endpoint only when live trading is intentional. <br>


## Reference(s): <br>
- [KIS Open API Endpoint Reference](references/kis-api-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/tgparkk/kis-trading) <br>
- [KIS production API endpoint](https://openapi.koreainvestment.com:9443) <br>
- [KIS mock trading API endpoint](https://openapivts.koreainvestment.com:29443) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown-oriented text with inline shell commands and command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KIS API credentials and a local config file; order commands support dry-run review before live submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
