## Description:

Public HTTP client skill exposing compute.* tools by calling a private Compute Gateway over HTTPS. Includes a starter kit to run OpenClaw preconfigured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aleksandrkrivolap](https://clawhub.ai/user/aleksandrkrivolap)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to let agents call a configured private Compute Gateway for session management, command execution, usage lookup, and artifact helper operations over HTTPS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger remote command execution through the configured Compute Gateway.

Mitigation: Install only with a trusted gateway, use a narrowly scoped and revocable API key, and require human confirmation or gateway-side policy for command execution.

Risk: Artifact deletion and session destruction operations can remove remote state.

Mitigation: Apply gateway-side authorization and confirmation policies for destructive operations.

Risk: The starter kit uses an overrideable, unpinned OpenClaw image while the official image and startup command remain unconfirmed.

Mitigation: Avoid the draft Docker starter kit in production until the image and command are pinned and verified.

Risk: The configured gateway URL and API token control access to private compute resources.

Mitigation: Use HTTPS-only gateway URLs and keep MCP_COMPUTE_API_KEY out of source control and logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aleksandrkrivolap/skills/openclaw-agent-compute)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript client code, shell commands, and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MCP_COMPUTE_URL and MCP_COMPUTE_API_KEY to call a trusted private Compute Gateway.]

## Skill Version(s):

0.1.7 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
