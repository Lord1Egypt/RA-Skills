## Description:

Manage ecommerce and local-service memberships, benefits, and expiry reminders across platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to track memberships across ecommerce and local-service platforms, monitor expiration dates and unused benefits, and estimate whether renewing a membership is worthwhile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Membership names, expiry dates, benefit counts, and spending estimates may be stored in local OpenClaw storage.

Mitigation: Use only in environments where local storage of this membership data is acceptable, and avoid entering sensitive account credentials or payment details.

Risk: Current prompts and outputs are primarily Chinese, which may make the skill less accessible to non-Chinese users.

Mitigation: Review outputs for comprehension when used by non-Chinese users or add localization before broader deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown or structured JSON-like summaries with membership records, alerts, benefit usage, and renewal-value recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local skill storage for membership names, expiry dates, benefit counts, and spending estimates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
