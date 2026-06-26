## Description: <br>
Detects the largest vehicle in a local image with TrafficEye car-box detection, runs make and model recognition for that vehicle, and returns license plates attached to the same road-user payload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eyedea-ai](https://clawhub.ai/user/eyedea-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect a user-provided vehicle image, select the largest detected road user, and return its box, make and model data, and associated license plate records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle images and detected license plate data are sent to TrafficEye during live recognition. <br>
Mitigation: Use the skill only when this data sharing is acceptable for the image and deployment context. <br>
Risk: TrafficEye API credentials are required for live requests. <br>
Mitigation: Use an environment-scoped API key, prefer header or bearer authentication, and avoid query-string credentials unless the deployment specifically requires them. <br>


## Reference(s): <br>
- [TrafficEye Homepage](https://trafficeye.ai) <br>
- [TrafficEye API Documentation](https://www.trafficeye.ai/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/eyedea-ai/make-and-model-recognition) <br>
- [eyedea-ai Publisher Profile](https://clawhub.ai/user/eyedea-ai) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the helper script, with agent-facing guidance for setup and interpretation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local image path and a TrafficEye API key for live recognition; offline validation can use the bundled sample response.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
