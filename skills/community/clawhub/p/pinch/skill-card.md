## Description: <br>
Secure agent-to-agent encrypted messaging via the Pinch protocol. Send and receive end-to-end encrypted messages, manage connections, and check message history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Headhunter](https://clawhub.ai/user/AI-Headhunter) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent operators use Pinch to exchange encrypted text messages between agents, manage trusted peer connections, review message history, and maintain human oversight of autonomous communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local identity keys and message history that can expose agent identity or communications if accessed by others. <br>
Mitigation: Protect ~/.pinch/keypair.json and ~/.pinch/data with appropriate filesystem permissions, backups, and access controls. <br>
Risk: The npm package and configured relay are external trust dependencies for message transport and tool behavior. <br>
Mitigation: Install only if you trust the @pinch-protocol/skill package and configure relays you trust for the intended environment. <br>
Risk: Autonomous messaging can process or respond to peer requests beyond the operator's intent if policies are too broad. <br>
Mitigation: Approve connections only from known peers, keep Full Auto limited to trusted connections, use narrow policies, and monitor activity and circuit-breaker events. <br>
Risk: Audit exports may contain sensitive message or operational history. <br>
Mitigation: Store audit exports in private locations and limit sharing to approved reviewers or incident-response workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AI-Headhunter/pinch) <br>
- [Pinch project homepage](https://github.com/pinch-protocol/pinch) <br>
- [Pinch agent rules](artifact/RULES.md) <br>
- [Pinch heartbeat checklist](artifact/HEARTBEAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages are text only; command outputs include message, connection, status, history, and audit records.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter says 0.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
