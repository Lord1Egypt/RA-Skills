## Description: <br>
Automatically detect and log health data (weight, blood sugar, exercise) to AX3 system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klcintw](https://clawhub.ai/user/klcintw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to detect health measurements in chat messages and record supported values such as weight, blood sugar, and running time to AX3. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ambiguous chat numbers can be interpreted as sensitive health records and sent to AX3 without clear opt-in or confirmation. <br>
Mitigation: Require explicit health keywords or units, confirm bare-number entries before logging, and tell users that detected measurements will be stored in AX3. <br>
Risk: Health measurements are sensitive personal data. <br>
Mitigation: Use this skill only when AX3 health auto-logging is intended and access to the AX3 logging path is appropriate for the user and deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/klcintw/health-auto-log) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON and confirmation text from a Python script, with markdown guidance for agent usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes a single message string and may call AX3 through mcporter when supported measurements are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
