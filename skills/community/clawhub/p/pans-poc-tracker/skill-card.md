## Description: <br>
Tracks AI compute sales proof-of-concept work across lifecycle stages, blockers, follow-up reminders, and conversion reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, solution engineering, and account teams use this skill to manage AI compute POC records, track stages and blockers, capture customer feedback, monitor follow-up needs, and generate status reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: POC and customer tracking records are stored locally as JSON and may contain sensitive business information. <br>
Mitigation: Install only where local storage is acceptable, treat the JSON file as sensitive business data, and avoid entering secrets. <br>
Risk: Update and close commands modify local POC records. <br>
Mitigation: Invoke record-changing commands deliberately and review the target POC ID before applying updates or closure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pans-poc-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI command examples and plain-text terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local POC records in JSON under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
