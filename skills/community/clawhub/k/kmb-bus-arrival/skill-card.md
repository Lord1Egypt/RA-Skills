## Description: <br>
Retrieves real-time KMB and LWB bus arrival information from the official Hong Kong ETA Bus API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenho1394](https://clawhub.ai/user/stevenho1394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer transit queries by looking up live KMB and LWB arrival times for a route and stop in Hong Kong. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OpenClaw tool definitions and README describe commands that the bundled script does not implement, so the skill may not work as advertised. <br>
Mitigation: Align the public tool definitions and README with the implemented getArrival command before deployment. <br>
Risk: The skill runs a local Python script and makes live network requests to data.etabus.gov.hk. <br>
Mitigation: Review the script before installation and allow outbound access only to the required public transit API endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevenho1394/kmb-bus-arrival) <br>
- [KMB ETA Bus API](https://data.etabus.gov.hk/v1/transport/kmb) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text with Markdown-style emphasis and bullet lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live API responses with no caching; availability depends on data.etabus.gov.hk.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
