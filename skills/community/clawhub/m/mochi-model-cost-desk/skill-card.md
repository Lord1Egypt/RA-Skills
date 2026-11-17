## Description:

Estimate model API costs from exported token usage and supplied rates, separating cached input, output and currencies. Use for Model API Cost Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and AI operators can estimate model API costs from selected token-usage exports and dated rates they supply, compare totals with optional budgets, and keep currencies separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Usage exports, reports, and local state may contain sensitive information.

Mitigation: Use only the selected usage export and dated rates needed for the estimate; keep the host sandbox enabled and remove reports or local state when no longer needed.

Risk: Estimates may differ from provider charges when rate units, cached-token treatment, or excluded fees are incomplete or inaccurate.

Mitigation: Record the rate date and source, confirm whether input counts include cached tokens, and treat results as estimates rather than official invoices.

## Reference(s):

- [Action contract (references/input.md)](references/input.md)
- [Model API Cost Desk on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-model-cost-desk)
- [MochiLab](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Analysis, JSON, HTML, CSV]

**Output Format:** [Cost summaries and report files in JSON, HTML, and CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates use supplied usage and rates, keep currencies separate, and do not represent official invoices.]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
