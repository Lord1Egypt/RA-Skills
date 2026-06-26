## Description: <br>
JF Tech Pro AI Smart Search helps an agent search JF Cloud Storage alarm videos by semantic keywords and retrieve matching video segments or playback URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video operations teams use this skill to search JF Tech cloud-stored camera or alarm videos by semantic terms, inspect matching clips, and retrieve playback URLs through JF Tech APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JF Tech credentials, device identifiers, device tokens, playback URLs, search terms, and video metadata may expose access to sensitive camera footage. <br>
Mitigation: Use credentials scoped to the intended account and device, keep secrets in environment variables, limit sharing of output, and treat returned URLs and metadata as private. <br>
Risk: A misconfigured endpoint could send credentialed requests somewhere other than the intended JF Tech service. <br>
Mitigation: Keep JF_ENDPOINT pointed at documented official JF Tech hosts such as api.jftechws.com or api-cn.jftech.com. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jftech/jftech-open-pro-ai-smart-search) <br>
- [JF Tech Open Platform](https://open.jftech.com/) <br>
- [JF Tech API Documentation](https://docs.jftech.com/) <br>
- [JF Tech AI Smart Search Documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557) <br>
- [JF Tech Cloud Playback Documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-like API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment variables for JF Tech credentials and returns search results, selected clip metadata, device token status, and playback URL guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
