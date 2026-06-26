## Description: <br>
Manage AI agent identities on the Live Neon platform by fetching identity, syncing content, running discovery, reviewing beliefs, and building prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to Live Neon, manage persistent agent identity, sync source content, run identity discovery, review proposed beliefs and responsibilities, and retrieve runtime prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can transmit user-derived observations, source quotes, synced content, and connected-account data to an external identity-discovery service. <br>
Mitigation: Do not send secrets, credentials, private customer text, regulated data, or confidential business context in observations, quotes, synced sources, or connected accounts. <br>
Risk: Approved beliefs and responsibilities can change an agent's runtime prompt and behavior. <br>
Mitigation: Review pending beliefs and responsibilities manually before approval and avoid approve-all workflows unless the proposed changes have been reviewed. <br>
Risk: Heartbeat or proactive reporting can create recurring third-party data transmission. <br>
Mitigation: Enable heartbeat or proactive reporting only where recurring transmission to Live Neon is acceptable for the deployment context. <br>


## Reference(s): <br>
- [Live Neon Persona ClawHub Page](https://clawhub.ai/liveneon/live-neon-persona) <br>
- [Live Neon Publisher Profile](https://clawhub.ai/user/liveneon) <br>
- [Live Neon Agent Homepage](https://persona.liveneon.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command-oriented guidance for registering, syncing, discovering, reviewing, and fetching Live Neon agent identity data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
