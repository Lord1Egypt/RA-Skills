## Description: <br>
Crypto trading signal, price prediction, and market analysis for Binance pairs using market data, news sentiment, scoring, verification, and reporting commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k2-l](https://clawhub.ai/user/k2-l) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto analysts use this skill to fetch Binance market data and crypto news, generate BUY/SELL/HOLD signal summaries, verify outcomes after 30 minutes, and review hit-rate history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes third-party market and news API calls that can consume quota or depend on revocable API keys. <br>
Mitigation: Use revocable API keys, configure only the credentials needed, and monitor NewsAPI usage limits. <br>
Risk: The scheduler can continue polling and consuming API quota if started unintentionally. <br>
Mitigation: Run the scheduler only intentionally, prefer dry-run first, and stop it when active monitoring is no longer needed. <br>
Risk: Crypto signal outputs may be mistaken for guaranteed trading outcomes. <br>
Mitigation: Treat generated BUY/SELL/HOLD results as research signals, review the summarized factors, and avoid adding exchange credentials unless needed. <br>


## Reference(s): <br>
- [Binance API endpoint](https://api.binance.com/api/v3) <br>
- [CryptoPanic API endpoint](https://cryptopanic.com/api/v1/posts/) <br>
- [NewsAPI endpoint](https://newsapi.org/v2/everything) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-facing guidance with shell commands and generated local JSON signal records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes market, news, signal, budget, verification, and report records locally; the scheduler can keep polling APIs until stopped.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
