## Description: <br>
AI-powered multilingual virtual salesperson for 24/7 global customer reception, client retention, real-time boss alerts, and continuous sales optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanlv123](https://clawhub.ai/user/zhanlv123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External-facing sales teams and business owners use this skill to create or update an Ieasysell AI reception link, support multilingual customer reception, synchronize visitor records, and receive follow-up notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the user to paste an Ieasysell browser Local Storage login token, which may grant session-level account access. <br>
Mitigation: Install only after trusting the publisher, use a dedicated or least-privileged account where possible, rotate or revoke the token if exposure is suspected, and avoid sharing the token outside the configured skill secret. <br>
Risk: The skill automatically syncs customer contact details and visitor records into local memory and notifications without clearly documented retention or deletion controls. <br>
Mitigation: Confirm retention, redaction, deletion, and access-control procedures before using the skill with real customers or regulated personal data. <br>
Risk: Background polling may continue to fetch visitor records on the configured interval. <br>
Mitigation: Confirm how to stop or disable polling before deployment, and monitor sync behavior after configuration changes or link resets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhanlv123/ieasysell) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown-style status messages with structured run results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a reception URL, digital human ID, visitor summaries, follow-up suggestions, sync status, and error-recovery guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
