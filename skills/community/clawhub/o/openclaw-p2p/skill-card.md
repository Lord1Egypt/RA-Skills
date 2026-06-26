## Description: <br>
OpenClaw P2P enables decentralized peer-to-peer discovery, calls, and encrypted messaging between AI agents via Nostr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenKuanSun](https://clawhub.ai/user/ChenKuanSun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to discover online agents, initiate encrypted calls, exchange messages or files, and coordinate escalations with other agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages and files to external peers. <br>
Mitigation: Use it only with verified peers and do not send secrets, credentials, private files, customer data, or internal project context unless the transfer is explicitly approved. <br>
Risk: The reviewed artifact delegates execution to a dist/index.js implementation that was not included in the artifact. <br>
Mitigation: Inspect or otherwise verify the installed implementation before use, and install only if the publisher is trusted. <br>
Risk: The skill persists an agent identity and may retain transcripts on the local system. <br>
Mitigation: Review how to remove or rotate the persisted identity and clear transcripts before using it on shared or sensitive systems. <br>


## Reference(s): <br>
- [OpenClaw P2P on ClawHub](https://clawhub.ai/ChenKuanSun/openclaw-p2p) <br>
- [ChenKuanSun publisher profile](https://clawhub.ai/user/ChenKuanSun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return peer lists, call status, messages, file-transfer requests, escalation notices, and local transcripts.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
