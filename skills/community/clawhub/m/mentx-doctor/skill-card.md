## Description: <br>
Mentx Doctor 医疗助手 helps agents submit health descriptions and medical files to the Mentx API to generate medical auxiliary decision reports with interim emotional support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dj801117](https://clawhub.ai/user/dj801117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users in mainland China and their agents use this skill to submit non-emergency health descriptions, medical images, and reports to Mentx for auxiliary medical decision reports. During report generation, the skill provides non-diagnostic emotional support and directs emergency symptoms away from online consultation. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health descriptions, medical files, reports, and identifiers may be sent to Mentx. <br>
Mitigation: Use only after explicit user agreement, limit uploads to intended medical files, and avoid sending unnecessary identifiers. <br>
Risk: The skill is not suitable for emergencies or urgent medical decision-making. <br>
Mitigation: Route emergency symptoms to local emergency services or urgent clinical care instead of using the skill. <br>
Risk: The Mentx API key may be exposed through local environment or shell history handling. <br>
Mitigation: Protect the MENTX_API_KEY value, avoid pasting it into shared logs, and rotate it if exposure is suspected. <br>
Risk: Temporary task files may retain medical API responses under /tmp/mentx-doctor. <br>
Mitigation: Clear /tmp/mentx-doctor after use, especially on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dj801117/mentx-doctor) <br>
- [Mentx developer documentation](https://developer.mentx.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell command examples and Mentx API response content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MENTX_API_KEY and may process user-provided medical descriptions, images, reports, and identifiers.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
