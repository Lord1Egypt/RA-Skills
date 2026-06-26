## Description: <br>
Reads script.json and character cards, then generates one Seedream 4.0 image-to-image keyframe per scene using each scene's character reference images to keep characters consistent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, comic production teams, and developers use this skill to convert a scene script and character manifests into vertical storyboard keyframes with consistent character references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project files can steer which local character images are uploaded to Volcengine and where outputs are written. <br>
Mitigation: Run in a dedicated project directory and inspect script.json plus character manifest image paths and scene IDs before execution. <br>
Risk: The workflow requires ARK_API_KEY and may incur paid image-generation charges. <br>
Mitigation: Use a budget-limited API key and monitor the skill's cost controls before running large storyboards. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhaobod1/huo15-comic-storyboard) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON] <br>
**Output Format:** [PNG storyboard images with a manifest JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates one 9:16 keyframe per scene and records output paths and prompts in manifest.json.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
