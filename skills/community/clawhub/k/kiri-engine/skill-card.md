## Description: <br>
Kiri Engine uses the KIRI Engine API to turn user-supplied videos or image sets into 3D models or 3D Gaussian Splatting assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taosiuman](https://clawhub.ai/user/taosiuman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to submit videos or image sets to KIRI Engine, monitor reconstruction jobs, and download generated 3D model or 3DGS assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected photos or videos, filenames, and task data are sent to KIRI Engine for processing. <br>
Mitigation: Avoid private, proprietary, or location-sensitive media unless the user accepts the third-party processing and temporary retention described by the skill. <br>
Risk: The skill requires a KIRI Engine API key. <br>
Mitigation: Store the API key only in the local user profile configuration file, avoid sharing it in prompts or logs, and rotate it if exposure is suspected. <br>
Risk: Generated model download links are time-limited and server-side assets are temporary. <br>
Mitigation: Download completed assets promptly and keep a local backup in the user-selected project directory. <br>


## Reference(s): <br>
- [KIRI Engine API documentation](https://gentlebandit.feishu.cn/wiki/PsHawWV0gi2jePkmRoycwMwXnIc) <br>
- [KIRI Engine API settings](https://www.kiriengine.com/api-settings) <br>
- [ClawHub skill page](https://clawhub.ai/taosiuman/kiri-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with PowerShell command examples and downloaded asset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce downloaded ZIP contents containing OBJ, FBX, GLB, USDZ, STL, PLY, or 3DGS assets depending on the selected reconstruction mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
