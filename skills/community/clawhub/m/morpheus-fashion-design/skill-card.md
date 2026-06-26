## Description: <br>
Generates professional fashion and product advertising images with AI models holding or wearing products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PauldeLavallaz](https://clawhub.ai/user/PauldeLavallaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, marketers, and agent operators use this skill to turn product and model images plus a campaign brief into commercial fashion or product advertising imagery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product photos, model face images, and campaign text may be uploaded to ComfyDeploy. <br>
Mitigation: Use the skill only when those inputs are approved for upload to ComfyDeploy. <br>
Risk: A local usage tracker may receive prompt and output metadata. <br>
Mitigation: Inspect or remove ~/clawd/scripts/track-usage.sh before running scripts/generate.py if that tracking is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PauldeLavallaz/morpheus-fashion-design) <br>
- [Model catalog repository](https://github.com/PauldeLavallaz/model_management) <br>
- [ComfyDeploy deployment queue API](https://api.comfydeploy.com/api/run/deployment/queue) <br>
- [ComfyDeploy file upload API](https://api.comfydeploy.com/api/file/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Guidance] <br>
**Output Format:** [PNG image file plus console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires product and model images, a campaign brief, a target audience, and a ComfyDeploy API key.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata; artifact frontmatter lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
