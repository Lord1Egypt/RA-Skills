## Description: <br>
CLI tool to store, retrieve, list, and clear conversation contexts per channel, user, or thread. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation authors use this skill to manually persist short conversation histories for custom scripts or integrations that need channel-, user-, or thread-scoped context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored conversation history is saved as plaintext under the skill data directory. <br>
Mitigation: Do not store secrets or sensitive personal data; review and protect the data directory according to your environment's access controls. <br>
Risk: Running the clear command without a channel can erase all contexts managed by this skill. <br>
Mitigation: Use scoped channel, user, or thread arguments when clearing context, and confirm backups or recovery expectations before bulk deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Derick001/multi-chat-context-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores context locally in plaintext JSON; no external dependencies beyond python3.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
