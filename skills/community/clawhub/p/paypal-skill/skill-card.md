## Description: <br>
Registers a PayPal skill for organizing public financial-service pages, product descriptions, rate rules, and help information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize publicly available PayPal product, rate, service-boundary, help-center, risk-notice, and support information. It is intended for information organization only, not account access, transaction execution, investment advice, or handling private financial data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public PayPal rates, product terms, risk notices, and help content may change over time or vary by region. <br>
Mitigation: Include the source page date, retrieval date, and applicable region when summarizing financial-service information. <br>
Risk: Summaries of PayPal public information could be mistaken for account, transaction, investment, lending, or tax advice. <br>
Mitigation: Keep outputs limited to public-information organization and state that the skill does not perform account operations, execute transactions, or provide financial advice. <br>
Risk: Requests may include private account, balance, identity, card, bank, or transaction data outside the skill boundary. <br>
Mitigation: Decline to process private or logged-in account data and use only publicly visible PayPal pages and notices. <br>


## Reference(s): <br>
- [PayPal homepage](https://www.paypal.com/) <br>
- [ClawHub skill page](https://clawhub.ai/mike47512/paypal-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries, tables, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite page dates and applicable regions when summarizing time-sensitive financial-service information.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
