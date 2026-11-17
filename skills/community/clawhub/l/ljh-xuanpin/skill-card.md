## Description:

Product selection judgment skill that guides a user through a five-step evidence check and returns a pursue, do-not-pursue, or collect-more-data verdict for an ecommerce candidate product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, product teams, and market analysts use this skill to evaluate whether a candidate product has sufficient category opportunity, market size, competitor weakness, review-backed pain points, and SKU potential before committing resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-run promotional messaging and external contact solicitation may be unwanted in some deployments.

Mitigation: Review the onboarding behavior before installation and use the skill only where that messaging is acceptable.

Risk: The skill may read and append local workspace dossier files when that workflow is enabled.

Mitigation: Run it only in workspaces where local dossier reads and writes are expected, and avoid providing confidential product or competitor data unless that storage behavior is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-xuanpin)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown product-selection report with tables, ratings, verdict, evidence gaps, and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May offer to save final deliverables and append conclusions to a local dossier when the user agrees.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
