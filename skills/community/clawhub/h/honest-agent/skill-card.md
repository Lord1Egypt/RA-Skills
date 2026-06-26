## Description: <br>
Honest Agent guides an agent to track commitments, check replies for unsupported claims, label media and file handling uncertainty, and persist audit records for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[141553](https://clawhub.ai/user/141553) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make an assistant record commitments, surface unfinished promises, and avoid presenting guesses or unverified media interpretations as facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist and replay conversation-derived commitments and audit entries. <br>
Mitigation: Install it only when persistent tracking is desired, avoid sensitive conversations unless this storage is acceptable, and review or clear memory/honest-agent/ as needed. <br>
Risk: Media and file handling may involve OCR or transcription tools that receive user-provided content. <br>
Mitigation: Use media recognition only with appropriate consent and data handling expectations, and disclose uncertainty when recognition or transcription is unavailable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, configuration, JSON files] <br>
**Output Format:** [Markdown guidance with JSON commitment and audit records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory/honest-agent/honest-commitments.json and memory/honest-agent/honest-logs.json when the hosting agent follows the skill instructions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
