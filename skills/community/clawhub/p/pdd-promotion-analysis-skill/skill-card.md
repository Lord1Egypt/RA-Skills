## Description:

Stages PDD promotion spreadsheets for paid server-side diagnostics, guides the user-directed Alipay payment flow, and renders the returned diagnostic report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw0830](https://clawhub.ai/user/sw0830)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, operators, and their agents use this skill to submit single-product PDD promotion data, complete the required paid analysis flow, and receive a server-generated diagnostic report with rendered output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads PDD promotion spreadsheets and optional operation logs to a remote paid analysis service.

Mitigation: Use the skill only after explicit user confirmation that the business data may be sent to aituiguangbao.com.

Risk: The skill stores local credentials and generated reports under ~/.pdd_skill.

Mitigation: Protect the local user account and delete ~/.pdd_skill credentials or reports when they are no longer needed.

Risk: Generated HTML reports should be treated as remote content.

Mitigation: Open reports in a constrained viewer or browser profile appropriate for untrusted HTML.

Risk: The paid analysis flow depends on a user-directed Alipay payment exchange.

Mitigation: Do not manually pass Payment-Proof values; follow the payment tool flow and preserve the request body emitted by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sw0830/skills/pdd-promotion-analysis-skill)
- [Server-resolved GitHub import](https://github.com/sw0830/sw0830/tree/main/pdd-promotion-analysis-skill%20-%20%E5%89%AF%E6%9C%AC)
- [Remote analysis service](https://aituiguangbao.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text and Markdown with shell command snippets; paid service responses can be rendered as HTML, Markdown, or JSON report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-directed Alipay payment before analysis results are returned.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; source skill frontmatter reports 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
