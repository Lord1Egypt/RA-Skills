## Description: <br>
Helps configure a four-agent healthcare triage workflow for patient intake, symptom analysis, appointment scheduling, and encounter records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and healthcare operations teams use this skill to set up coordinated Pilot agents for intake, triage routing, scheduling, and record handling in a healthcare workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive patient data while the release evidence says it overstates HIPAA readiness and omits basic privacy and deployment safeguards. <br>
Mitigation: Use only synthetic data until encryption, access controls, audit retention, credential handling, EHR/calendar agreements, and legal/compliance approval have been verified; do not treat HIPAA wording as proof of compliance. <br>


## Reference(s): <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-healthcare-triage-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown instructions with bash commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, and a running daemon; generated configuration uses role and hostname placeholders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
