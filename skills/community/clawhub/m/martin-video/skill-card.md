## Description: <br>
Generate MP4 videos using SkillBoss API Hub with customizable duration, aspect ratio, optional model hints, and optional image input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate video clips from prompts and optional reference images, then save the generated result as a local MP4 file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, and the SKILLBOSS_API_KEY are sent to SkillBoss API Hub. <br>
Mitigation: Install only if you trust SkillBoss, avoid sensitive media or secrets in prompts and images, and use a rotatable API key. <br>
Risk: The script saves generated video to the requested local filename. <br>
Mitigation: Use a dedicated output filename or directory to reduce accidental overwrite risk. <br>


## Reference(s): <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/martin-video) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [MP4 file with console status text and a MEDIA path line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; accepts prompt, filename, duration, aspect ratio, optional model hint, and up to three input images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
