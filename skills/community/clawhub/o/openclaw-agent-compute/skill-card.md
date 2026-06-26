## Description: <br>
Public HTTP client skill exposing compute.* tools by calling a private Compute Gateway over HTTPS. Includes a starter kit to run OpenClaw preconfigured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aleksandrkrivolap](https://clawhub.ai/user/aleksandrkrivolap) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent call a private Compute Gateway for session management, command execution, usage lookup, and artifact operations over HTTPS. The bundled starter kit helps configure OpenClaw to use the compute gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad remote command execution through a private Compute Gateway. <br>
Mitigation: Install only against a trusted, controlled gateway and require explicit approval for exec operations. <br>
Risk: Artifact and session controls can upload, download, delete artifacts, or destroy compute sessions. <br>
Mitigation: Use gateway-side path restrictions, command restrictions, least-privilege revocable API keys, logging, and usage limits. <br>
Risk: The starter kit uses an overrideable OpenClaw image and draft configuration that are not fully pinned. <br>
Mitigation: Pin the container image and confirm the OpenClaw config schema before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aleksandrkrivolap/openclaw-agent-compute) <br>
- [README](README.md) <br>
- [Starter kit README](starter-kit/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript code references, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCP_COMPUTE_URL and MCP_COMPUTE_API_KEY for gateway access.] <br>

## Skill Version(s): <br>
0.1.7 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
