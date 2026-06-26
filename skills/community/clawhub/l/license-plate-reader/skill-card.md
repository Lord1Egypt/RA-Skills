## Description: <br>
Detect and read the largest license plate from an image using the TrafficEye REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[radekzc](https://clawhub.ai/user/radekzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit a local vehicle image to TrafficEye and extract the largest detected license plate payload, including OCR text, country/type, geometry, scores, occlusion, and unreadable indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle images and license plate data may be privacy-sensitive when sent to TrafficEye or a configured compatible endpoint. <br>
Mitigation: Use the skill only with images you are authorized to process, avoid sensitive people, locations, or business context, and confirm the configured API endpoint is trusted. <br>
Risk: API credentials and endpoint settings control where images and plate data are transmitted. <br>
Mitigation: Keep TRAFFICEYE_API_KEY private and scope TRAFFICEYE_API_URL and related authentication settings to the intended service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/radekzc/license-plate-reader) <br>
- [TrafficEye homepage](https://trafficeye.ai) <br>
- [TrafficEye API reference](https://www.trafficeye.ai/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the selected plate payload from the TrafficEye response; offline validation can use the bundled sample response JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
