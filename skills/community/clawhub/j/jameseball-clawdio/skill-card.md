## Description: <br>
Secure P2P communication for AI agents. Noise XX handshake, XChaCha20-Poly1305 encryption, connection consent, human verification. Zero central servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamesEBall](https://clawhub.ai/user/JamesEBall) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Clawdio to set up encrypted peer-to-peer messaging, task delegation, and sub-agent communication across machines or networks without a central server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security-sensitive defaults and trust handling may be weaker than the skill's secure messaging claims. <br>
Mitigation: Review before installing and test in an isolated environment before relying on it for sensitive agent communication. <br>
Risk: Automatic peer acceptance can allow unintended peers in non-test environments. <br>
Mitigation: Keep autoAccept disabled outside isolated tests and require explicit consent for unknown inbound peers. <br>
Risk: Listening on a remotely reachable interface can expose the node to unintended connection attempts. <br>
Mitigation: Bind to 127.0.0.1 or firewall the configured port unless remote access is intentional. <br>
Risk: Peer identity trust depends on out-of-band verification for high-trust use. <br>
Mitigation: Compare peer safety numbers out of band before marking a peer human-verified. <br>
Risk: Persisted identity files contain sensitive identity material. <br>
Mitigation: Avoid persisting sensitive identities until the identity file is protected and outbound peer-key binding is fixed. <br>


## Reference(s): <br>
- [Clawdio release page](https://clawhub.ai/JamesEBall/jameseball-clawdio) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent in creating Clawdio nodes, exchanging connection strings, sending encrypted agent messages, and configuring consent, verification, identity persistence, and liveness checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
