## Description: <br>
One-click photo to 3D model pipeline that uses Gemini to generate a clean isometric view from a photo, then uses the Tripo3D API to convert it into a GLB 3D model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m15010495895-sudo](https://clawhub.ai/user/m15010495895-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and 3D content creators use this skill to turn supported image files into 3D asset outputs for prototyping, game assets, product renders, or AR workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are sent to Gemini and Tripo3D services. <br>
Mitigation: Avoid private, sensitive, confidential, or rights-restricted images unless the provider policies have been reviewed. <br>
Risk: The workflow uses external API quota and service credentials. <br>
Mitigation: Use dedicated API keys where possible and review generated outputs before downstream use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m15010495895-sudo/photo-to-3d) <br>
- [Gemini API key setup](https://aistudio.google.com/apikey) <br>
- [Tripo3D platform](https://platform.tripo3d.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Terminal status text plus generated PNG and GLB files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and TRIPO_API_KEY; selected images are sent to Gemini and Tripo3D services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
