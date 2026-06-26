## Description: <br>
Looks up a bank card's issuing bank, card type, location, and customer service details through Juhe's API for single or batch queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer requests such as identifying which bank issued a card, whether it is a debit or credit card, and what province or city is associated with it. It can process one card number or a small batch and return human-readable summaries, tables, and JSON details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank card numbers and the Juhe API key may be sent to a third-party service over plain HTTP. <br>
Mitigation: Use only after explicit user confirmation, avoid passing the API key on the command line, prefer environment or .env configuration, and do not use the skill until HTTP transmission is addressed. <br>
Risk: The skill depends on Juhe service availability, API-key validity, and request quota; lookups can fail or time out. <br>
Mitigation: Handle reported errors plainly, retry timeouts once, and avoid treating lookup results as the sole source for financial or identity decisions. <br>


## Reference(s): <br>
- [Juhe Bank Card API documentation](https://www.juhe.cn/docs/api/id/305) <br>
- [Juhe data platform](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown or terminal text with JSON result blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JUHE_BANKCARDCODE_KEY; accepts one or more 15-19 digit bank card numbers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
