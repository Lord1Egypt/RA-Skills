## Description: <br>
Generate or edit images using the Google Gemini API through the nanobanana command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feiskyer](https://clawhub.ai/user/feiskyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to generate new images or edit local input images by prompting Google Gemini from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected local images are sent to Google Gemini under the user's Gemini API account. <br>
Mitigation: Avoid confidential or sensitive prompts and images, use an isolated Python environment, and prefer a restricted API key where possible. <br>
Risk: The security summary notes under-disclosed Google Search and thought-output features. <br>
Mitigation: Review commands before execution and confirm that the documented nanobanana.py workflow is acceptable for the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/feiskyer/nanobanana-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and can save generated or edited images to a user-specified output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
