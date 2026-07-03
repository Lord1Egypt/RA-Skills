## Description: <br>
Jd helps users view JD Clinic booking guidance, open clinic pages, submit appointment requests, consult customer service, query prices, and find BeautsGO app download links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Patients and clinic booking assistants use this skill to navigate JD Clinic information on BeautsGO, collect appointment details, submit booking requests, and route users to pricing or support channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Appointment details such as phone number, requested time, and party size may be sent to external services without a clearly documented final confirmation step. <br>
Mitigation: Review the flow before installation and require explicit user confirmation before submitting appointment details. <br>
Risk: The security evidence reports hardcoded API tokens in the published artifact. <br>
Mitigation: Rotate exposed tokens and move service credentials to publisher-managed secret storage before relying on the skill in production. <br>
Risk: The authoritative security verdict is suspicious. <br>
Mitigation: Use only after reviewing the publisher, the BeautsGO booking workflow, and the data handling expectations for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beautsgo/jd-clinic-booking) <br>
- [Publisher profile](https://clawhub.ai/user/beautsgo) <br>
- [JD Clinic booking page](https://i.beautsgo.com/cn/hospital/jd-clinic/skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted text responses with booking guidance, links, price summaries, and appointment status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Chinese and English responses; may open external BeautsGO pages or submit appointment details to external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, skill metadata, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
