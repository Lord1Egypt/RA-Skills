## Description:

Generates one Chinese nickname or a de-duplicated batch using optional style and length filters, with Markdown, plain-text, and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and people choosing an online nickname can generate Chinese name suggestions, optionally filtering by style or length and reproducing results with a seed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writing with --output overwrites an existing file at the chosen path.

Mitigation: Choose a new path or confirm the target file can be replaced.

Risk: A custom morpheme pool without entries for a selected style can relax style matching.

Mitigation: Review any fallback notice or provide matching morphemes for each slot used by the selected patterns.

Risk: Generated nicknames are not checked for availability, trademarks, or sensitive terms.

Mitigation: Review a suggestion for conflicts and suitability before adopting or publishing it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-nickname-generate)
- [Usage Guide](artifact/references/usage-guide.md)
- [Verification Method](artifact/references/verification-method.md)
- [Data Flow Diagram](artifact/references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown, plain text, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One nickname by default, or up to 20 distinct suggestions; optional seed, style, and length filters.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
