## Description:

Navil Audit runs deep security audits for OpenClaw by scanning MCP servers, installed skills, and agent configuration, then producing severity-ranked findings and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanpantheon](https://clawhub.ai/user/ivanpantheon)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, security reviewers, and operators use this skill to audit OpenClaw and MCP deployments, evaluate attack exposure, and generate remediation-oriented security reports. It can also support CI/CD security gates and compliance review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs the external navil PyPI package while assessing sensitive agent and MCP configuration.

Mitigation: Install only when the publisher and package are trusted, prefer a pinned and hash-verified package version, and run audits with a clearly specified target.

Risk: Security scans can expose credentials, broad filesystem context, or unrelated configuration if run with excessive access.

Mitigation: Run the audit in a constrained environment and avoid exposing unrelated credentials, broad home-directory access, or unnecessary network access during scans.

Risk: Broad activation wording could lead to scans over a wider scope than the user intended.

Mitigation: Confirm audit scope before running scan or pentest commands, especially in workspaces with multiple skills, MCP servers, or production configuration.

## Reference(s):

- [Navil GitHub Repository](https://github.com/navilai/navil)
- [Navil CI/CD Integration Guide](https://github.com/navilai/navil#cicd-integration)
- [Navil Audit ClawHub Page](https://clawhub.ai/ivanpantheon/skills/navil-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with severity-ranked findings, tables, remediation steps, and inline shell commands; may include guidance for JSON or SARIF scanner output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes scan and pentest results, including security scores, finding counts, attack simulation outcomes, and top remediation actions.]

## Skill Version(s):

1.0.2 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
