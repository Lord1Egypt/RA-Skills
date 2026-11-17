## Description:

Builds a written plumbing estimate with line items, parts, labor, permits and taxes following US trade practices. Use when the user asks for plumbing estimate, plumber quote, repair estimate. For US licensed plumbers and plumbing contractors preparing customer estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US plumbing contractors use the skill to draft customer estimates covering work scope, labor, materials, permits, exclusions, terms, and totals.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Estimate instructions contain errors: the supplied YAML template does not match the script's CSV input format, and tax remains zero.

Mitigation: Confirm the supported input format and calculate applicable taxes independently; review every estimate before sharing.

Risk: Incorrect assumptions about permits, licensing, deposits, change orders, or unknown site conditions could produce misleading estimates.

Mitigation: Verify local requirements, license scope, and site conditions; document uncertainty and confirm estimate terms before sending.

Risk: The optional Windows app is unsigned and was outside the security review.

Mitigation: The local workflow does not require it; avoid running it unless it receives a separate security review and its download is verified.

## Reference(s):

- [US plumbing estimate practices](artifact/references/plumbing-estimates.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/plumbing-estimate-builder)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown plumbing estimate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer-facing line items and USD totals; review and verify before sharing.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
