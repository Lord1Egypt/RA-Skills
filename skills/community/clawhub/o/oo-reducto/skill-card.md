## Description:

Use Reducto to search and read data, including extracting structured data, parsing documents, and splitting documents into sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other document users can use their connected Reducto account to extract structured data, parse supported documents, and split documents into named sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute a changing remote installer without clear approval or limits on local changes.

Mitigation: Prefer manually installing a verified CLI release, require approval for local setup changes, check skill-synchronization settings, and send only documents authorized for OOMOL and Reducto to process.

## Reference(s):

- [Reducto documentation](https://docs.reducto.ai/)
- [Reducto](https://reducto.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-reducto)

## Skill Output:

**Output Type(s):** [Structured data, Text, API Calls]

**Output Format:** [JSON containing extracted data or parsed document content, chunks, blocks, and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and input; extraction uses a caller-supplied JSON Schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
