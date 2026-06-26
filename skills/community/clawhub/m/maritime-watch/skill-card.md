## Description: <br>
This is an unfinished prototype intended to monitor Chornomorsk port status by aggregating weather, vessel, security, and news data into a report. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[ApacheUA](https://clawhub.ai/user/ApacheUA) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts can inspect this prototype as a starting point for a port-status monitoring skill; it should not be used for real port, vessel, weather, news, or security decisions until implemented and validated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact advertises real-time port and security monitoring but the current script is not implemented. <br>
Mitigation: Use only for inspection or development until named data providers, input handling, validation, and tested JSON output are added. <br>
Risk: The script contacts placeholder URLs and does not document real outbound data sources. <br>
Mitigation: Replace placeholders with approved providers, document outbound requests, and review network behavior before connected use. <br>
Risk: Operational users could mistake placeholder output for verified maritime, weather, news, or security intelligence. <br>
Mitigation: Require human review and cross-source validation before using any future output for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ApacheUA/maritime-watch) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Intended JSON status report; current shell script emits a plain text placeholder.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a port name conceptually, but the current artifact uses placeholder URLs and does not return tested JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
