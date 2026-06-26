## Description: <br>
Calculates tiered GPU compute quotes using customer scale, contract duration, and prepayment discounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, finance, and infrastructure teams can use this skill to estimate GPU compute quotes across supported GPU models and compare discount scenarios before commercial review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded GPU prices and discount rules may produce quotes that do not match current commercial terms. <br>
Mitigation: Review and update the pricing table and discount rules before using generated quotes commercially. <br>
Risk: The broad trigger phrase may activate this skill for quote requests outside GPU compute pricing. <br>
Mitigation: Confirm the request is for supported GPU pricing before relying on the generated quote. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dashiming/pans-pricing-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text quote tables, JSON pricing data, and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quotes are based on hardcoded GPU prices and discount rules in the release artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
