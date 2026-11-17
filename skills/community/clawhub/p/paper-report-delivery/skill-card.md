## Description:

Builds and maintains daily paper-report delivery pipelines that collect and select papers, generate Chinese summaries and innovation analysis, produce readable HTML and Telegram message chunks, archive outputs, and deliver with retry and fallback behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanwu-fan](https://clawhub.ai/user/fanwu-fan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate daily paper and news digest workflows, including paper selection, Chinese report generation, readable HTML output, Telegram-ready text fallback, local archiving, and resilient Telegram delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image metadata can point to arbitrary local files that may be embedded into reports and sent to Telegram.

Mitigation: Restrict image metadata to a trusted image directory, reject absolute paths and traversal, and enforce image type and size checks before embedding.

Risk: Telegram delivery may send reports to an unintended destination if the target is not explicitly configured and verified.

Mitigation: Set and verify the Telegram destination before sending, and keep delivery targets configurable rather than hard-coded.

Risk: Local report archives may contain report content and embedded images that should not be broadly shared.

Mitigation: Store archives in controlled locations, review generated files before distribution, and apply an appropriate retention policy.

## Reference(s):

- [Paper Report Delivery Workflow](references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/fanwu-fan/skills/paper-report-delivery)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, JSON message caches, and HTML, Markdown, and PDF report artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local report files and Telegram delivery commands; messages are chunked for Telegram-sized delivery, and HTML delivery retries before falling back to text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
