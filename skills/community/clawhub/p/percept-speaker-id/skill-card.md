## Description: <br>
Identifies and tracks speakers in multi-person conversations, mapping speaker labels to names and managing voice command authorization levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis563](https://clawhub.ai/user/jarvis563) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Percept users use this skill to attribute multi-person conversation transcripts to known speakers and control which speakers may trigger voice commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local speaker identity and authorization records may expose sensitive information or grant command access to the wrong person if mishandled. <br>
Mitigation: Restrict access to the Percept dashboard and percept/data/speakers.json, and review owner and approved entries carefully. <br>
Risk: Outdated or incorrect speaker mappings can misattribute speech or authorization status. <br>
Mitigation: Delete or correct stale speaker mappings and periodically review the speaker registry. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jarvis563/percept-speaker-id) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Text] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helps maintain local speaker identity, owner, and authorization records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
