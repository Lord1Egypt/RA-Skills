## Description:

Release metadata identifies this skill as gpu-cluster-monitor, but the artifact implements a Docker-based browser scraper for YouTube and dynamic web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sounderliu](https://clawhub.ai/user/sounderliu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents can use the artifact to collect text or transcript-like content from authorized public URLs, especially YouTube pages and dynamic sites. Review the release-name mismatch before presenting this as a GPU cluster monitoring skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse arbitrary targets from inside Docker with weak isolation and unclear safeguards.

Mitigation: Use only on authorized public URLs, run in an isolated container and network, make mounts read-only where possible, and review or pin the Docker image and dependencies before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON printed to stdout with status, content type, source identifiers, and scraped text fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact truncates extracted transcript or page text before output.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact package.json says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
