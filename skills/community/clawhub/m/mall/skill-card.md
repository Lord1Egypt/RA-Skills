## Description: <br>
A shopping assistant skill that recognizes shopping intent, shows a fixed product catalog, helps users choose items and quantities, summarizes the cart, and hands confirmed orders to a separate payment skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sayxxx](https://clawhub.ai/user/sayxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to browse a small fixed catalog, build a cart, confirm an order total, and then delegate payment creation to a separate payment skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment creation and payment handling are delegated to a separate payment skill. <br>
Mitigation: Review the payment skill and provider separately before deployment, and preserve the explicit user confirmation step before payment handoff. <br>
Risk: Incorrect product selection, price display, or total calculation could lead to an inaccurate order. <br>
Mitigation: Use only the fixed catalog from the artifact, calculate subtotals from listed prices and quantities, and show the order summary for confirmation before invoking payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sayxxx/mall) <br>
- [Publisher profile](https://clawhub.ai/user/sayxxx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Conversational Markdown with product lists, cart summaries, confirmation prompts, and payment handoff details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before payment handoff; does not collect address or contact details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
