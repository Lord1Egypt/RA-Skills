## Description:

Run request suites with status, JSON, header and latency assertions and compare regression reports. Use for API Testbench.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and engineers use the skill to run API request suites, check status, JSON, header, and latency assertions, and compare saved reports for regressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials supplied through environment variables are sent to the configured endpoints.

Mitigation: Review endpoint URLs and requested environment variables before running the suite; use credentials only with intended endpoints.

Risk: Write requests or requests to private hosts can affect unintended targets.

Mitigation: Authorize write requests and private-host access only for the specific intended targets.

## Reference(s):

- [Action contract](artifact/references/input.md)
- [API Testbench on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-api-testbench)
- [MochiLab](https://mochilab.bz)
- [MochiLab assistant setup](https://mochilab.bz/Skills/Connect.aspx?lang=en)

## Skill Output:

**Output Type(s):** [JSON, HTML, CSV, Text]

**Output Format:** [JSON command result and local JSON/HTML reports, with optional CSV; the agent can summarize pass/fail results and regressions in text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports omit response bodies and credential headers; results are stored in the active workspace.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
