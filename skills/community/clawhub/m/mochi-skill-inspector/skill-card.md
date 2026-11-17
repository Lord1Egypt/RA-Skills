## Description:

Inspect a Skill ZIP without executing it: archive boundaries, executable/network indicators and per-file hashes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and agent operators use this skill to inspect a selected Skill ZIP before installation, review archive paths and static indicators, and obtain per-file SHA-256 hashes without running package code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static indicators can be incomplete, and some indicators may be false positives.

Mitigation: Treat the report as a preliminary review aid; do not treat a clean result as approval or certification.

Risk: Inspecting untrusted ZIP files can expose the surrounding workspace to risk.

Mitigation: Use a sandboxed workspace and select only the ZIP files intended for inspection. Do not install or execute inspected packages as part of the review.

## Reference(s):

- [Inspection action contract](artifact/references/input.md)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-skill-inspector)
- [MochiLab homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [JSON, HTML]

**Output Format:** [JSON and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include archive file hashes and static review indicators; findings are not a safety certification.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
