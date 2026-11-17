## Description:

Local security self-check for your Windows PC and OpenClaw server setup (password protection, port, and exposure), producing a local report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawvincent](https://clawhub.ai/user/openclawvincent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and OpenClaw users use this skill to audit Windows and OpenClaw security posture, check update status, review server configuration, and generate local HTML or JSON reports for authorized systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network scans and optional credential or leak checks can affect systems outside the user's authorization.

Mitigation: Run active checks only against systems you own or are explicitly allowed to test, and keep credential and leak checks disabled unless needed.

Risk: Generated reports may contain sensitive local security, configuration, token, credential, or exposure details.

Mitigation: Store reports privately, do not publish output/ files, and share reports only through a secure destination when explicitly required.

Risk: Optional npm and MSRC lookup flags make external requests.

Mitigation: Use online lookup flags only when external network access is acceptable for the environment.

Risk: The included mock server is intended for isolated testing.

Mitigation: Do not run the mock server outside an isolated test environment.

## Reference(s):

- [OpenClaw PC Security README](artifact/README.md)
- [Example usage](artifact/examples/example.md)
- [MSRC CVRF API](https://api.msrc.microsoft.com/cvrf/v2.0/cvrf/{cid})

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, code]

**Output Format:** [Markdown guidance with shell commands and generated local HTML/JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated under output/ and may contain sensitive local security information.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
