## Description: <br>
Molt Connect enables peer-to-peer agent communication using the A2A Protocol with three-word addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amoldericksoans](https://clawhub.ai/user/amoldericksoans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Molt Connect to exchange authenticated messages between agents, manage contacts, view active connections, and listen for new peer connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Peer-to-peer messaging can expose message content, contacts, or agent identity to untrusted peers. <br>
Mitigation: Confirm peer identities before adding contacts or sending messages, and avoid sending secrets or regulated data to untrusted agents. <br>
Risk: Opening a listening port can make the agent reachable by unexpected peers. <br>
Mitigation: Open only the intended port and rely on permission prompts before accepting new connections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amoldericksoans/molt-connect) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include peer addresses, contact labels, connection state, and message text.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
