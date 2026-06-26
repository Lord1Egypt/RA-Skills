## Description: <br>
Configures an OpenClaw instance to use a local OpenAI-compatible text-to-speech backend with cloned voice mapping, test clip generation, troubleshooting, and LAN or Tailscale exposure guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotfinity](https://clawhub.ai/user/lotfinity) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to wire OpenClaw speech synthesis to a local TTS backend, verify model and voice selection, generate test clips, troubleshoot delivery, and expose the backend only when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent OpenClaw TTS configuration changes can redirect speech synthesis to an unintended local backend. <br>
Mitigation: Review OpenClaw config values before and after changes, and use the documented config set/get commands instead of editing config files directly. <br>
Risk: Exposing the TTS service port to LAN or Tailscale can allow unintended network access. <br>
Mitigation: Expose the port only when remote access is needed, confirm the listener binding, and restrict access with firewall rules or Tailscale ACLs. <br>
Risk: Test audio sent through channel plugins can reach unintended recipients. <br>
Mitigation: Confirm recipient and target IDs before sending generated clips through external channels. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user-directed OpenClaw CLI configuration, direct API test commands, listener checks, and channel-delivery troubleshooting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
