## Description: <br>
Communicate with other OpenClaw agents on your local network for synchronous questions, asynchronous task delegation, and peer reachability checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielithomas](https://clawhub.ai/user/danielithomas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let trusted OpenClaw agents ask peer agents questions, delegate longer-running work, check reachability, and list configured peers on a local network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and delegated tasks to peer agents, so misuse can expose sensitive information or trigger actions through an untrusted peer. <br>
Mitigation: Configure only trusted peers and avoid delegating prompts that contain secrets or actions you would not trust the receiving agent to perform. <br>
Risk: Cross-host communication over raw LAN HTTP can expose traffic or tokens if the transport is not secured. <br>
Mitigation: Keep gateways on loopback where possible and use SSH tunnels, TLS reverse proxies, or Tailscale Serve for encrypted transport. <br>
Risk: The peers.json file contains peer addresses and bearer tokens that are security-sensitive. <br>
Mitigation: Keep peers.json private, restrict file access, and rotate tokens if they may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielithomas/lobsterlan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text responses and status output produced by shell commands using JSON-over-HTTP requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a private peers.json configuration with trusted peer addresses and tokens.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
