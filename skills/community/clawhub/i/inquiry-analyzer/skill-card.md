## Description:

Analyzes Alibaba International inquiries over a selected time window, extracts product, customer, country, status, and background-check fields, and generates structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likem90is-cmd](https://clawhub.ai/user/likem90is-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operators and business analysts use this skill to review Alibaba inquiry activity, classify requested products, capture customer and country details, and merge inquiry and OKKI background reports for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in browser and can access Alibaba inquiry and OKKI background data.

Mitigation: Install only after source review, use a dedicated OpenClaw browser profile, and avoid running it on shared machines.

Risk: Generated reports, chat transcripts, and debug dumps can contain sensitive customer information.

Mitigation: Use restricted local output folders, avoid cloud-synced directories, clear reports and debug dumps after use, and request redaction or opt-in debug dumps before deployment.

Risk: The release evidence reports a hard-coded browser relay token.

Mitigation: Remove or rotate the token and prefer environment-based secret handling before operational use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/likem90is-cmd/skills/inquiry-analyzer)
- [Alibaba inquiry message center](https://message.alibaba.com/message/default.htm#feedback/all?order=%7B%22order%22%3A%22desc%22%2C%22orderBy%22%3A%22gmt_create%22%7D&pageSize=100)
- [Alibaba product management](https://i.alibaba.com/prod/product_manage#/product/online)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and CSV report files with supporting command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local inquiry, chat, CSV, OKKI, and merged report artifacts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
