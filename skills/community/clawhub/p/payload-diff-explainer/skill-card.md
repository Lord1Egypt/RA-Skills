## Description:

Compare two JSON payloads or API responses and explain the meaningful differences in plain English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheeseqi](https://clawhub.ai/user/cheeseqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare old versus new JSON payloads, API responses, config objects, request bodies, or raw diffs and understand the meaningful structural, value, and likely impact changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided API payloads can contain secrets, tokens, cookies, customer data, or other sensitive values.

Mitigation: Redact sensitive values before sharing payloads for analysis.

Risk: Likely impact can be uncertain when the payloads do not include enough business or UI context.

Mitigation: Call out uncertainty and validate conclusions against the relevant application behavior or domain rules.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with summaries, grouped differences, likely noise, and likely impact notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill analyzes only user-provided content and does not call external APIs, run production queries, or access internal systems.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
