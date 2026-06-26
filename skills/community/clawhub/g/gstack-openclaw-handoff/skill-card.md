## Description: <br>
Compact the current conversation into a structured handoff document for another agent or fresh session to continue the work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilmych](https://clawhub.ai/user/ilmych) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill when ending a long session, switching agents, or handing work to another teammate or fresh session. It produces a concise handoff that captures the goal, current state, decisions, open threads, artifacts, suggested skills, and context not captured elsewhere. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated handoff may include sensitive details from the conversation or be written to a temporary local file. <br>
Mitigation: Review the handoff before sharing or reusing it, avoid including secrets or private customer data, and delete the temporary file when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilmych/gstack-openclaw-handoff) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown handoff document saved to a temporary local file, with the file path reported to the user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The handoff should reference existing files or URLs instead of duplicating large content and should redact secrets, tokens, passwords, and personal data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
