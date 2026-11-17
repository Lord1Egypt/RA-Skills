## Description:

Search and read bioRxiv and medRxiv preprints, retrieve preprint versions, and look up related publication and usage statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and other users can use this skill to find bioRxiv and medRxiv preprints, review preprint versions, and retrieve submission or publication statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unpinned remote installer code and add persistent agent changes through automatic skill synchronization.

Mitigation: Review the setup first, use a reviewed version-pinned CLI installation, and inspect the skill synchronization controls before enabling them.

Risk: Research requests pass through OOMOL and may consume credits.

Mitigation: Consider this routing when submitting research queries and monitor OOMOL credit usage.

## Reference(s):

- [bioRxiv](https://www.biorxiv.org/)
- [bioRxiv API documentation](https://api.biorxiv.org/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Research results and statistics as returned data with explanatory text; shell commands for invoking actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and its live input/output schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
