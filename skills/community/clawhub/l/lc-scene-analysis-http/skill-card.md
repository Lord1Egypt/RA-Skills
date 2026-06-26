## Description: <br>
Analyzes static construction-site images for safety hazards through configured HTTP endpoints, using data collection or cross-verification endpoints only when explicitly requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenqu108](https://clawhub.ai/user/chenqu108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and construction-safety teams use this skill to submit static construction-site image URLs for hazard identification, concise findings, structured collection output, or cross-verification when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured auth profile may point to an untrusted or inappropriate API provider. <br>
Mitigation: Confirm lc_scene_http:default uses a trusted provider before installation or use. <br>
Risk: API credentials or local authentication profile contents could be exposed if mishandled. <br>
Mitigation: Keep the API key secret and minimally scoped, and do not display tokens, Authorization headers, or auth profile contents. <br>
Risk: Construction-site images may contain sensitive operational or personal information. <br>
Mitigation: Avoid sending sensitive images unless the API provider's privacy and retention practices are acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenqu108/lc-scene-analysis-http) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Markdown or structured JSON-style text, depending on the requested endpoint and response mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves key hazard conclusions, avoids exposing API keys or auth profile contents, and reports missing input, service errors, timeouts, or abnormal responses instead of fabricating results.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
