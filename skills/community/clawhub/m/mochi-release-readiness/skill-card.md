## Description:

Check a release manifest for valid versions, checksums and recorded passing tests before a human publication decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release teams use this skill to check a release manifest for version, checksum and recorded test-status issues before making a human publication decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A manifest with valid version, checksum and test-status fields does not establish that files or tests are genuine, or that a release is publicly available.

Mitigation: Independently verify the files, signatures, installation, test evidence and public downloads before deciding to publish.

## Reference(s):

- [Input contract](references/input.md)
- [Chinese usage notes](references/zh-CN.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-release-readiness)

## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [JSON report and workspace artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs offline and writes new files under exports/ in the selected workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
