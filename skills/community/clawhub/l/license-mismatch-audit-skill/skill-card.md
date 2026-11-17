## Description:

Benign audit fixture for testing whether skill directories and marketplaces accept frontmatter-only license metadata.

This skill is for research and development only.

## Publisher:

[xmy0416](https://clawhub.ai/user/xmy0416)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace reviewers use this test-only skill to check whether skill platforms accept license metadata without a bundled license file and to summarize the limits of self-declared license metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package does not include a LICENSE file, so downstream users may not be able to verify licensing terms from repository files alone.

Mitigation: Verify the release license against repository files, publisher identity, and project history before relying on it for distribution or compliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xmy0416/skills/license-mismatch-audit-skill)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown or plain text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No shell commands, network access, credential access, install hooks, or file modification workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
