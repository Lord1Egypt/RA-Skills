## Description:

Checks Chinese invoice authenticity and details from invoice code, number, issue date, amount, check code, and related fields using the JisuAPI invoice verification service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance operations agents use this skill to verify invoice validity and retrieve seller, buyer, tax, amount, status, and line-item details. It can also list supported invoice types before a verification request is made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice details and the JisuAPI app key are sent to a third-party service for verification.

Mitigation: Use the skill only for invoice data the user is authorized to share with JisuAPI, and avoid including tax, business, or personal data that should not leave the user's environment.

Risk: Verification depends on JisuAPI account status, quota, permissions, network availability, and service responses.

Mitigation: Confirm JISU_API_KEY is configured for the invoice verification API and treat API errors, quota limits, or maintenance responses as inconclusive rather than proof that an invoice is invalid.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/invoiceverify)
- [JisuAPI invoice verification documentation](https://www.jisuapi.com/api/invoiceverify/)
- [JisuAPI website](https://www.jisuapi.com/)
- [Invoice verification API endpoint](https://api.jisuapi.com/invoiceverify/verify)
- [Invoice type API endpoint](https://api.jisuapi.com/invoiceverify/type)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests Python package, and the JISU_API_KEY environment variable.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
