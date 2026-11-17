## Description:

Build a courier station AI chat system with Express, GPT-5.5, local JSON DB, OCR, and WeChat-style frontend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and parcel-station operators use this skill to build a chat-based package lookup and OCR intake application for pickup-code, tracking-tail, and phone-tail workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive shipment data and OCR uploads may expose personal information if deployed without privacy controls.

Mitigation: Define consent, provider choice, logging, retention, and deletion rules before enabling OCR on real waybills.

Risk: Package-management pages and APIs could allow unauthorized access or changes if left open.

Mitigation: Require authenticated admin access for management pages and package APIs.

Risk: Public lookup responses may reveal more shipment detail than a customer needs.

Mitigation: Restrict lookup responses to the minimum information required to complete pickup support.

Risk: The local JSON database can contain sensitive parcel and recipient data.

Mitigation: Protect the local database with appropriate filesystem permissions, backups, and operational controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code blocks and API/interface specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes implementation guidance for an Express service, local JSON storage, OCR handling, and a WeChat-style frontend.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
