## Description: <br>
Queries JD International logistics tracking data and supply-chain or cross-border parcel performance indicators for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdl-external-skills](https://clawhub.ai/user/jdl-external-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External logistics and operations users use this skill to check international shipment tracking details, supply-chain operating metrics, and cross-border parcel fulfillment performance. Agents use it to map natural-language requests to supported parameters, run the bundled Node.js query scripts, and summarize returned logistics data without fabricating missing values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token-backed API calls can expose sensitive logistics credentials if the token is over-privileged, logged, or reused outside this skill. <br>
Mitigation: Use a dedicated, least-privilege JD logistics token, keep it in the runtime environment rather than prompts or shared files, and rotate it after exposure or publisher changes. <br>
Risk: The bundled scripts disable TLS certificate verification, which weakens protection for shipment and operations data sent to external APIs. <br>
Mitigation: Remove rejectUnauthorized:false and require normal certificate validation before using real shipment, customer, or business data. <br>
Risk: Shipment identifiers and operations metrics are sent to JD/Ochama API endpoints during lookups. <br>
Mitigation: Confirm what data categories are approved for these APIs and avoid submitting restricted customer or shipment data until the maintainer documents data handling expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jdl-external-skills/i-logisitics-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jdl-external-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command templates and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a JD logistics token in the runtime environment and returns shipment or operations data from external JD/Ochama APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
