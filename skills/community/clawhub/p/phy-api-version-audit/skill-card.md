## Description:

API versioning health auditor that scans REST API source code for unversioned routes, deprecated endpoints missing Sunset headers, hardcoded version strings, mixed versioning strategies, and version gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before deployment to audit REST API source code for versioning consistency, deprecation headers, hardcoded client version strings, and route version gaps. It is intended for source-code reviews of API services across common backend frameworks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads source code under the requested root path.

Mitigation: Run it only on repositories or services the agent is intended to inspect, and scope the root path to the smallest relevant project area.

Risk: Claims for Koa, NestJS, JAX-RS, Chi, Sinatra, Slim, and custom whitelist behavior are unreliable until fixed.

Mitigation: Manually verify results for those frameworks or behaviors before relying on the audit output.

## Reference(s):

- [Canlah AI Homepage](https://canlah.ai)
- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-api-version-audit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown-style audit report with grouped findings, framework-specific fix snippets, and a CI fail-gate command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports HIGH, MEDIUM, and LOW severity findings; supports a root path and CI-oriented severity gate.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
