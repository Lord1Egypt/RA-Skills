## Description: <br>
Complete training plan solution for My Likes platform that fetches historical data, analyzes training patterns, generates personalized plans, converts them to Likes format, and pushes them to the calendar for running, cycling, swimming, and strength training. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenwynn](https://clawhub.ai/user/chenwynn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Athletes, coaches, and OpenClaw users use this skill to retrieve My Likes training data, analyze recent activity, generate structured training plans, preview plan JSON, and push plans to individual or group calendars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write or overwrite training plans for one or more My Likes accounts. <br>
Mitigation: Review generated plan JSON before pushing, use preview or dry-run flows where available, and avoid bulk or overwrite operations unless authorized and backed up. <br>
Risk: The installer documentation includes curl-to-bash installation and the security evidence flags this as risky. <br>
Mitigation: Prefer manual installation from the released artifact and inspect scripts before execution. <br>
Risk: The skill stores and uses a My Likes API key and can export activity or GPS data. <br>
Mitigation: Use the least-privileged API key available and treat exported data plus local API-key files as sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenwynn/grouptraining) <br>
- [Likes Open API Documentation](artifact/references/api-docs.md) <br>
- [Likes Training Code Format Reference](artifact/references/code-format.md) <br>
- [Sport-Specific Training Examples](artifact/references/sport-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON plan examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a LIKES_API_KEY and may read or write My Likes activity, feedback, and calendar plan data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
