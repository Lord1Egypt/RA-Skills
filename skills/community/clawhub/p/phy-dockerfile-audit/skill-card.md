## Description:

Phy Dockerfile Audit is a zero-dependency Dockerfile static security auditor that scans Dockerfiles for common container risks and can fail CI on critical or high findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and security engineers use this skill to scan Dockerfiles locally or in CI for common container security misconfigurations mapped to CIS Docker Benchmark and CWE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scanner output is advisory and may need project-specific review before remediation.

Mitigation: Review findings before acting on them and validate changes against the project's container security requirements.

Risk: One remote ADD checksum remediation example is flawed if copied verbatim.

Mitigation: Download remote content to a file, compare it against a pinned trusted digest using a valid sha256sum manifest, and fail the build on mismatch.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, terminal text, JSON, or GitHub Actions annotations depending on selected CLI format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can operate locally without Docker, hadolint, network access, or third-party Python dependencies.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
