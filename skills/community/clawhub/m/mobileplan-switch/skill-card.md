## Description: <br>
Helps users lower mobile costs by moving a primary number to a low-cost carrier retention plan and comparing secondary high-data SIM-card options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanqj1218](https://clawhub.ai/user/yanqj1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Consumers use this skill to compare carrier downgrade options, prepare customer-service scripts, and choose a secondary high-data SIM-card plan by budget and province. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends a third-party SIM-card application flow where users may be asked for sensitive identity and shipping details. <br>
Mitigation: Review the application link and provider independently before submitting personal data, and do not provide name, ID number, phone number, or address unless the enrollment page is trusted. <br>
Risk: Carrier plan availability, prices, and eligibility may vary by region, contract status, and current carrier policy. <br>
Mitigation: Confirm plan terms directly with the carrier before changing service or applying for a new SIM card. <br>


## Reference(s): <br>
- [Carrier retention-plan guide](artifact/references/carriers.md) <br>
- [High-data SIM-card recommendations](artifact/references/data-cards.md) <br>
- [ClawHub listing](https://clawhub.ai/yanqj1218/mobileplan-switch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with tables, scripts, and optional URL or QR-code command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations may include carrier scripts, budget tiers, regional plan notes, and third-party application links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
