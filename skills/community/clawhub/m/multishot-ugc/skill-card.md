## Description: <br>
Generate 10 perspective/angle variations from a single image for multi-shot UGC videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators and developers preparing UGC-style promotional videos use this skill to turn one hero image into multiple angle variations for scene selection and downstream lip-sync or video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads input images to ComfyDeploy for cloud processing, which can expose sensitive personal or proprietary content to a third-party service. <br>
Mitigation: Use only images approved for ComfyDeploy processing and avoid sensitive personal or proprietary content unless that processing is acceptable. <br>
Risk: Security evidence says downloaded filenames are not safely contained. <br>
Mitigation: Run the skill in a low-impact workspace and review or sanitize downloaded filenames before trusting generated files. <br>
Risk: The skill requires a ComfyDeploy API key and makes authenticated cloud API calls. <br>
Mitigation: Use a limited ComfyDeploy API key and avoid sharing credentials in prompts, logs, or committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PauldeLavallaz/multishot-ugc) <br>
- [ComfyDeploy API endpoint](https://api.comfydeploy.com/api/run/deployment/queue) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, API Calls, Guidance] <br>
**Output Format:** [PNG image files with terminal status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 10 perspective variations from one input image; default output is 2K, 9:16 PNG files.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
