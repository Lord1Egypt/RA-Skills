## Description: <br>
Find and cancel unwanted subscriptions by analyzing bank transactions. Detects recurring charges, calculates annual waste, and provides cancel URLs. CSV-based analysis with optional Plaid integration for ClawdBot users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chipagosfinest](https://clawhub.ai/user/Chipagosfinest) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to audit bank transaction history for recurring subscription charges, estimate annual spend, categorize what to keep or cancel, and receive cancellation links and guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Plaid integration can transmit bank transaction data to Plaid's API. <br>
Mitigation: Prefer CSV mode for local processing unless Plaid is intentionally enabled and the user understands the data flow. <br>
Risk: Broad triggers such as saving money could activate the subscription audit unexpectedly. <br>
Mitigation: Use narrow, explicit prompts for subscription audits and confirm user intent before analyzing financial transaction data. <br>
Risk: Cancellation guidance may affect financial services or memberships if acted on without review. <br>
Mitigation: Provide URLs and guidance only; require the user to navigate manually and make each cancellation decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Chipagosfinest/just-fucking-cancel) <br>
- [Common Services - Cancellation Guide](references/common-services.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, HTML, Guidance] <br>
**Output Format:** [Markdown guidance plus an interactive HTML audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recurring-charge summaries, user categorization, cancellation URLs, privacy toggle behavior, and manual cancellation guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
