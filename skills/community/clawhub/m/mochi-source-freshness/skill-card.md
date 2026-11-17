## Description:

Compare explicitly dated sources with a research cutoff and flag stale, undated or future-dated records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and researchers use this skill to assess whether supplied sources fall within a requested freshness window and identify undated or future-dated records. It helps organize review; it does not verify source claims or website changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Freshness labels may be mistaken for verification of factual claims or changes to the original website.

Mitigation: Consult the original source before relying on important claims; the helper evaluates only the dates provided.

Risk: Generated local reports retain the supplied source details.

Mitigation: Provide only details needed for the request and handle the resulting reports appropriately.

## Reference(s):

- [Input contract](references/input.md)
- [中文用法](references/zh-CN.md)
- [MochiLab homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Files]

**Output Format:** [JSON result and local report with source freshness labels and generated artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Labels are based on supplied dates; factual claims and website changes are not verified.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
