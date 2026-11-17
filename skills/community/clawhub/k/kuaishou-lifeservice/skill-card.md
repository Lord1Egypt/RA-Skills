## Description:

Helps Kuaishou Life Service merchants and developers query merchant accounts, stores, staff, products, authorization status, and business operation data through Kuaishou merchant APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingfeng9924](https://clawhub.ai/user/qingfeng9924)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and developers use this skill to configure Kuaishou merchant credentials, call Kuaishou Life Service merchant APIs, inspect product and store data, and generate merchant performance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide Kuaishou merchant app keys, merchant IDs, app secrets, and access tokens, which can expose merchant business data if mishandled.

Mitigation: Use a protected secret store or disposable test credentials, avoid pasting production secrets into chat or shell history, and rotate any credential that may have been pasted or logged.

Risk: The artifact stores merchant secrets and cached access tokens in plaintext files under .kuaishou-localife-token.

Mitigation: Restrict workspace access, exclude .kuaishou-localife-token from source control and backups, and delete cached tokens when they are no longer needed.

Risk: The authoritative security verdict is suspicious because the skill handles merchant credentials and business data in unsafe plaintext ways.

Mitigation: Review credential-handling behavior before installation and grant access only in environments where this data exposure is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qingfeng9924/skills/kuaishou-lifeservice)
- [Kuaishou Open Platform](https://open.kwailocallife.com/)
- [Kuaishou Life Service OpenAPI Reference](references/api-reference.md)
- [Merchant Diagnosis Report Notes](references/report-notes.md)
- [Kuaishou Merchant API Base](https://lbs-open.kuaishou.com)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown, JSON, and command-line output from Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Kuaishou merchant credentials or an access token; some reports are limited to a maximum 31-day date range.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
