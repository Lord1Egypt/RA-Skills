## Description:

Generates customized loan telemarketing scripts from product details and customer profiles, including opening hooks, value framing, qualification questions, product presentation, objection handling, and close prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g620710](https://clawhub.ai/user/g620710)

### License/Terms of Use:

MIT-0

## Use Case:

External loan-sales teams use this skill to prepare structured telemarketing scripts for consumer loans, business loans, mortgages, refinancing, and related loan products. It is intended to support script drafting, onboarding, and A/B testing, with human review for financial compliance before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can send API keys and customer-related inputs to a plaintext HTTP SaaS endpoint with unclear ownership.

Mitigation: Do not use real customer personal data, regulated financial information, or confidential product strategy unless the publisher provides HTTPS, clear service ownership, privacy terms, and matching documentation.

Risk: The documented DeepSeek workflow does not match the script behavior reported by the security evidence.

Mitigation: Review the runtime script and endpoint behavior before installation, and verify that deployed behavior matches the approved workflow.

Risk: The TELE_SCRIPT_USER_KEY may be exposed when used with the default HTTP endpoint.

Mitigation: Treat any key used with the default endpoint as exposed, rotate it before further use, and avoid sending credentials over non-HTTPS endpoints.

Risk: Loan telemarketing content can create financial compliance risk if used without review.

Mitigation: Review generated scripts against applicable financial advertising, lending, consent, and customer-data rules before calling customers.

## Reference(s):

- [Opening Hooks](references/opening_hooks.md)
- [Objection Handling](references/objection_handling.md)
- [Compliance Rules](references/compliance_rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON responses, with optional saved text files from the generator script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts are organized into six modules and may include compliance reminders, objection responses, and close prompts.]

## Skill Version(s):

1.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
