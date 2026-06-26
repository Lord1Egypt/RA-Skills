## Description: <br>
Queries Kdniao's API for real-time shipment tracking events and helps agents present delivery status and progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15814059255](https://clawhub.ai/user/15814059255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support agents handling shipment inquiries use this skill to look up a tracking number through Kdniao, parse the returned logistics timeline, and summarize the current delivery status for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes real-looking Kdniao API credential examples that may be copied or treated as valid secrets. <br>
Mitigation: Configure your own Kdniao credentials, do not reuse the example values, and rotate any credential that may have been exposed. <br>
Risk: Shipment tracking numbers and request data are sent to Kdniao's external API during lookups. <br>
Mitigation: Run lookups only when authorized to share the tracking data with Kdniao and avoid sending unrelated sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/15814059255/kdniaoapi-skill) <br>
- [Kdniao production API endpoint](https://api.kdniao.com/api/dist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KUAIDI_BIRD_API_CREDENTIALS and a shipment tracking number; sends lookup requests to Kdniao's external API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
