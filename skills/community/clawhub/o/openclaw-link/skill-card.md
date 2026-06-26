## Description: <br>
Cross-instance agent communication for OpenClaw, enabling multiple sessions to discover peers, delegate tasks, share findings, exchange files, and coordinate work through a relay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharoonsharif](https://clawhub.ai/user/sharoonsharif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect trusted OpenClaw sessions across a local machine or LAN, coordinate multi-agent workflows, delegate work, share discoveries, and exchange collaborative files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Networked task delegation can allow unintended agents to join or influence work if the relay is exposed without adequate access control. <br>
Mitigation: Keep the relay bound to localhost when possible; require a strong shared token for LAN use and avoid unauthenticated all-interface binding. <br>
Risk: Internet tunnels or cross-network use can expose relay traffic beyond the trusted environment. <br>
Mitigation: Use HTTPS or WSS, authentication, and network access controls before exposing the relay outside a trusted local network. <br>
Risk: Incoming delegated tasks, broadcasts, and shared files may contain untrusted instructions or misleading content. <br>
Mitigation: Review incoming tasks and shared files before acting on them, and keep users informed when networked agent communication is active. <br>


## Reference(s): <br>
- [ClawLink Protocol Reference](references/protocol.md) <br>
- [Openclaw Link package page](https://clawhub.ai/sharoonsharif/openclaw-link) <br>
- [Publisher profile](https://clawhub.ai/user/sharoonsharif) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-to-agent task, message, and shared-file workflow guidance; runtime data is described as in-memory relay state.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
