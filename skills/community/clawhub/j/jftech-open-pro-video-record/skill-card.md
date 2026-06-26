## Description: <br>
Lists JFTech device cloud and local recordings and retrieves playback or download URLs for authorized camera video. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query JFTech camera recording history, retrieve cloud or local recording lists, and obtain playback or download links for authorized devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JFTech application secrets and device passwords can expose access to camera recording resources. <br>
Mitigation: Store credentials only in environment variables, protect JF_APPSECRET and JF_PASSWORD, and use least-privilege credentials for authorized devices. <br>
Risk: Playback and download URLs may expose sensitive video content while valid. <br>
Mitigation: Avoid sharing printed URLs, limit access to authorized users, and handle returned links as sensitive material. <br>
Risk: A misconfigured endpoint can send requests outside the intended JFTech API hosts. <br>
Mitigation: Keep JF_ENDPOINT on an official JFTech host such as api.jftechws.com or api-cn.jftech.com. <br>


## Reference(s): <br>
- [JFTech Open Platform](https://open.jftech.com/) <br>
- [JFTech API Documentation](https://docs.jftech.com/) <br>
- [Cloud Video List API](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=66142b2ca13c418d84085772a627d650) <br>
- [Cloud Playback URL API](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=2e08468f46564602d01ae8a244661672) <br>
- [Skill Release Page](https://clawhub.ai/jftech/jftech-open-pro-video-record) <br>
- [Publisher Profile](https://clawhub.ai/user/jftech) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Terminal text or JSON containing recording metadata and playback or download URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JFTech environment-variable credentials and authorized device access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
