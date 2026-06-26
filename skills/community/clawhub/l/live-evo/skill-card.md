## Description: <br>
Self-evolving memory system that learns from verifiable tasks, retrieves relevant past experiences, and generates task-specific guidelines for coding, prediction, and analysis work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mercury7353](https://clawhub.ai/user/Mercury7353) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve prior task experiences, synthesize task-specific guidance, and update a local experience store after verifiable outcomes or feedback. It is most applicable to coding, analysis, prediction, debugging, and problem-solving tasks where feedback can improve future attempts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently saves and reuses task details in a local cross-task memory database without clear opt-in, redaction, retention, or deletion controls. <br>
Mitigation: Avoid use with secrets, credentials, personal data, regulated information, or proprietary code unless entries are manually sanitized before storage. <br>
Risk: Stored experiences may contain information the user does not want reused in later tasks. <br>
Mitigation: Review the local ~/.live-evo experience store periodically and remove experiences that should not be reused. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and plain-text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task-specific guidelines from local experience records and may update a persistent local JSONL experience database.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
