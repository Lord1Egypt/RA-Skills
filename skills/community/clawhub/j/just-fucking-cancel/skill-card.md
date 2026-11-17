## Description:

Find and cancel unwanted subscriptions by analyzing bank transactions. Detects recurring charges, calculates annual waste, and provides cancel URLs. CSV-based analysis with optional Plaid integration for ClawdBot users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipagosfinest](https://clawhub.ai/user/chipagosfinest)

### License/Terms of Use:


## Use Case:

External users use this skill to analyze bank transaction exports or optional Plaid-connected transactions, identify recurring subscriptions, categorize which ones to keep or cancel, and receive an HTML audit with cancellation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank transaction exports can contain sensitive financial activity.

Mitigation: Prefer the CSV workflow for local processing and review generated reports before sharing or copying subscription details.

Risk: Optional Plaid integration transmits transaction data to Plaid and requires credentials.

Mitigation: Configure Plaid credentials only in trusted runtimes with appropriate secret handling, or leave Plaid variables unset for CSV-only use.

Risk: Subscription classifications and cancellation guidance may need user confirmation before action.

Mitigation: Review the audit manually and use the provided URLs as guidance; the skill does not perform automated cancellation.

## Reference(s):

- [Common Services Cancellation Guide](references/common-services.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with cancellation URLs and an HTML audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include subscription classifications, annualized cost estimates, privacy-aware report controls, and manual cancellation tips.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
