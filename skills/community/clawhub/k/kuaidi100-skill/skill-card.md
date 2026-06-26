## Description: <br>
Queries Kuaidi100 logistics APIs for shipment tracking, carrier identification, shipping cost estimates, and delivery time estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuaidi100-api](https://clawhub.ai/user/kuaidi100-api) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer parcel tracking, carrier lookup, shipping cost, and delivery-time questions through the Kuaidi100 API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment details are sent to the Kuaidi100 API service. <br>
Mitigation: Use the skill only when sending shipment information to Kuaidi100 is acceptable, and confirm ambiguous logistics requests before running it. <br>
Risk: Some tracking requests may require sensitive details such as a phone number or address information. <br>
Mitigation: Avoid providing phone numbers or full addresses unless required for the requested carrier or estimate. <br>
Risk: Configured API credentials could be exposed or overused if shared broadly. <br>
Mitigation: Use a dedicated revocable Kuaidi100 API key and store it in the provided config or KUAIDI100_API_KEY environment variable. <br>


## Reference(s): <br>
- [Kuaidi100 API Open Platform](https://api.kuaidi100.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/kuaidi100-api/kuaidi100-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/kuaidi100-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown returned from API-backed command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include logistics traces, carrier identifiers, cost estimates, delivery estimates, and quota or API-key setup guidance.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
