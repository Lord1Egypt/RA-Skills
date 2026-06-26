## Description: <br>
Real-time chat between Kiro instances via shared JSON file with polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonerbo](https://clawhub.ai/user/sonerbo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate two or more Kiro instances by sending, reading, and polling messages through a shared local JSON chat file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages persist in a shared plaintext JSON file. <br>
Mitigation: Do not send secrets through the chat file, and install only when local plaintext chat history is acceptable. <br>
Risk: Received messages are untrusted input and polling loops can continue longer than intended. <br>
Mitigation: Review messages before acting on them and stop polling when coordination is finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sonerbo/kiro-realtime) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON chat records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Messages include sender, recipient, timestamp, content, and read status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
