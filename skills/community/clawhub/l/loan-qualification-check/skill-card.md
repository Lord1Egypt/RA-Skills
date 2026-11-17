## Description:

Evaluates loan applicant qualifications through a paid service and returns estimated borrowing capacity, product matches, rejection risks, and approval probability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g620710](https://clawhub.ai/user/g620710)

### License/Terms of Use:

MIT-0

## Use Case:

External loan brokers and lending advisors use this skill to pre-screen applicants, estimate likely loan capacity, compare product fit across consumer, business, mortgage, and car loan categories, and prepare follow-up guidance. Results are preliminary and should not be treated as final lender approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applicant financial details and the user key may be sent to a remote service over the plaintext HTTP default.

Mitigation: Use the skill only after configuring a trusted HTTPS endpoint and confirming provider privacy, retention, and consent requirements.

Risk: Loan recommendations and approval estimates can be mistaken for final lending decisions.

Mitigation: Present results as preliminary screening guidance and require review against current lender policies and applicant documentation.

Risk: The user key functions as a credential for paid evaluations and account functions.

Mitigation: Store LOAN_CHECK_USER_KEY securely, avoid logging it, and rotate or revoke it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g620710/skills/loan-qualification-check)
- [Loan product list](artifact/references/product_list.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [CLI output as text or JSON, with documentation examples for Markdown reports and saved files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and LOAN_CHECK_USER_KEY; evaluations consume service credits and may send applicant financial details to the configured loan-check service.]

## Skill Version(s):

2.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
