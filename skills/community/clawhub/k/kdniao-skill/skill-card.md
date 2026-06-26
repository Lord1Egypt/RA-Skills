## Description: <br>
Queries Kdniao shipment tracking through the Kdniao API and returns courier status and tracking events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15814059255](https://clawhub.ai/user/15814059255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to look up package delivery status, track waybill progress, and summarize shipment events from Kdniao using their own API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment tracking numbers and Kdniao credentials are sent to the configured API endpoint. <br>
Mitigation: Use only trusted Kdniao endpoints, avoid overriding the API URL unless the destination is trusted, and confirm users are comfortable sending tracking numbers to Kdniao. <br>
Risk: The documentation includes a realistic-looking credential example. <br>
Mitigation: Replace sample credentials with the user's own secret and avoid publishing real credentials in documentation, terminal history, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/15814059255/kdniao-skill) <br>
- [Kdniao API endpoint used by the skill](https://api.kdniao.com/api/dist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KUAIDI_BIRD_API_CREDENTIALS in CUSTOMER_CODE|APP_KEY format and a shipment tracking number.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
