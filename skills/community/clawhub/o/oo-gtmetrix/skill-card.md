## Description:

Operate a connected GTmetrix account to inspect account data and run performance tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GTmetrix users use this skill to inspect account status, pages, reports, and test options, and to start performance tests through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code that was not verified and may automatically synchronize additional agent skills.

Mitigation: Review setup before installing; use a separately approved, verified CLI release and consider disabling automatic agent-skill synchronization.

Risk: Performance tests may consume credits through the connected GTmetrix account.

Mitigation: Review the test request and use the skill's confirmation step before starting a test.

## Reference(s):

- [GTmetrix API documentation](https://gtmetrix.com/api/docs/2.0/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance, Shell commands]

**Output Format:** [JSON responses with concise text summaries and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can retrieve account data or start a performance test.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
