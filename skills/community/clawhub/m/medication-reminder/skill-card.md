## Description: <br>
Track medications with dosing schedules and intake history. Use when managing prescriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to record medication names, doses, frequencies, and intake history through local shell commands. It is a lightweight tracker and should not be relied on as a dependable medication reminder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder features are incomplete, so the skill may not reliably indicate when medication is due. <br>
Mitigation: Use it only as a local log and verify medication timing with a dependable reminder system or clinician-provided schedule. <br>
Risk: Medication details and intake history are stored in plaintext local files. <br>
Mitigation: Enter medication details only if plaintext storage in the home directory is acceptable, and protect or delete the data directory as needed. <br>


## Reference(s): <br>
- [Medication Reminder on ClawHub](https://clawhub.ai/bytesagain1/medication-reminder) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files] <br>
**Output Format:** [Plain text command output and JSON Lines files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores medication and intake records under ~/.local/share/medication-reminder/.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
