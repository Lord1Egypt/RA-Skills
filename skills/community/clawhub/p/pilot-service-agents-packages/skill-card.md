## Description:

Package-registry metadata for npm, PyPI, and Maven Central through Pilot Protocol service agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and dependency analysts use this skill to query package version, maintainer, dependency, and release metadata from npm, PyPI, and Maven Central service agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package names, dependency-analysis queries, and free-text summaries may be sent through the Pilot Protocol service-agent network.

Mitigation: Avoid submitting confidential dependency lists or proprietary package names unless the deployment environment and summary processing path are acceptable.

Risk: The packages agents provide metadata only and do not perform vulnerability scanning.

Mitigation: Use a dedicated vulnerability or CVE workflow when security findings are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-packages)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to retrieve normalized package-registry metadata through pilotctl inbox responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
