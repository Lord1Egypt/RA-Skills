## Description:

Identify conflicting and expired user-selected facts before proposing changes to an agent memory file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and agent users use this skill to review user-selected, sourced memory facts, identify conflicts and expired entries, and prepare a report before making separate memory changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports retain submitted fact values and source labels locally.

Mitigation: Submit only facts intended for review, and review the generated report before sharing it or making separate memory changes.

## Reference(s):

- [Input contract](references/input.md)
- [Chinese usage notes](references/zh-CN.md)
- [MochiLab homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Local JSON report with current facts, conflicts, and expired keys]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conflicting facts remain visible; source files and agent memory are not modified.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
