## Description:

Collects JD.com product details and reviews through the AI Data Platform for product selection and review analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

External users can collect JD.com product details and reviews for product selection and customer review analysis. Collection requests use platform points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic product-analysis prompts may trigger JD data collection outside its intended scope, and the security evidence is incomplete.

Mitigation: Use only when JD collection is intended, review broader product-analysis requests before invoking it, check balance and estimated cost before batch jobs, and review the skill scope before installation.

## Reference(s):

- [AI Data Platform](https://zlh.aidata366.com)
- [ClawHub skill page](https://clawhub.ai/cuiyunhai/skills/jd-data)

## Skill Output:

**Output Type(s):** [JSON data, Files, API Calls]

**Output Format:** [JSON responses, optionally saved to files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product details or paginated review data; large responses can be saved locally.]

## Skill Version(s):

1.6.7 (source: server release evidence, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
