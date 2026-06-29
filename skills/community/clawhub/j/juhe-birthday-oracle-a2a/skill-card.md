## Description: <br>
This skill lets agents run paid Juhe birthday-oracle lookups for a specified date, sending only the requested date to Juhe and returning structured birthday book, password, flower-language, and fortune-style results after Alipay payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and consumer agents use this skill to request paid entertainment-oriented birthday information for a specific date through Juhe, with Alipay payment confirmation before the query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill may initiate a paid Alipay-mediated query. <br>
Mitigation: Require explicit user confirmation after disclosing the fee, payment method, and privacy behavior before continuing. <br>
Risk: The query sends the user-provided birthday or date to Juhe. <br>
Mitigation: Send only the requested date for the lookup and do not collect or transmit unrelated personal data. <br>
Risk: Birthday interpretations are entertainment content and may be mistaken for factual or decision-grade advice. <br>
Mitigation: Present results as reference and entertainment only, not as guidance for major personal, career, health, or relationship decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-birthday-oracle-a2a) <br>
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown report with payment-flow guidance and API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a specific date; sends only the date to Juhe; payment is handled through an Alipay payment skill.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
