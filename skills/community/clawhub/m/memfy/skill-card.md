## Description: <br>
Capture durable user-approved memory when the user says memfy, without storing secrets or transient chatter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiwithenoch](https://clawhub.ai/user/aiwithenoch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Memfy to persist concise, durable notes for future sessions after explicit memory-style requests. It is intended for stable preferences, project facts, decisions, paths, and outcomes, while excluding raw secrets and transient chatter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable memory can preserve sensitive or no longer accurate details if the user asks the agent to remember them. <br>
Mitigation: Save only stable, user-approved facts; avoid raw credentials and sensitive personal data unless the user clearly permits and it is necessary. <br>
Risk: The skill writes to a local memory file, so a poorly chosen destination could mix unrelated context or surprise future sessions. <br>
Mitigation: Set MEMFY_MEMORY_FILE for an explicit destination, append rather than overwrite, and review the saved entry after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiwithenoch/memfy) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown memory entries and brief confirmation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append dated bullet points to a user-selected durable memory file; MEMFY_MEMORY_FILE can set the destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
