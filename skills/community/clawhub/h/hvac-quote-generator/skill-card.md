## Description:

Builds itemized US HVAC replacement and repair quotes with parts, labor, tax, deposit and warranty lines the customer can sign. Use when the user asks for hvac quote generator, hvac replacement estimate, air conditioner quote template. For US residential HVAC contractors and the office managers who prepare their quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US residential HVAC contractors and office managers use this skill to prepare itemized replacement or repair estimate drafts and organize customer, equipment, labor, tax, deposit, warranty, and exclusion details. It also helps identify state-specific tax, licensing, permit, and contract terms that must be confirmed before a contractor issues a quote.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The estimate generator does not follow the documented input format and uses a fixed tax rate, which can produce inaccurate customer quotes.

Mitigation: Treat generated estimates as drafts; verify all parsed line items, applicable local tax rates and taxable amounts, and totals before issuing any quote.

Risk: The optional Windows toolkit is a separate unsigned download and has not been reviewed as part of the Python workflow.

Mitigation: Prefer the Python workflow; do not download or run the Windows toolkit unless it receives a separate security review.

## Reference(s):

- [HVAC quoting rules](references/hvac-quote-rules.md)
- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/hvac-quote-generator)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Markdown, Configuration]

**Output Format:** [Itemized Markdown estimate and YAML quote brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer-specific amounts, tax treatment, and contract details require contractor confirmation.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
