## Description: <br>
Create, inspect, process, and optimize image files and visual assets with reliable format choice, resizing, compression, color-profile, metadata, and platform-export checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to choose image workflows and produce guidance or commands for resizing, converting, compressing, cropping, metadata handling, accessibility, and destination-specific exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image processing commands can overwrite originals or apply a bad batch transform across many files. <br>
Mitigation: Work on copies or explicit output paths, review overwrite and batch flags, and spot-check representative files before processing a full set. <br>
Risk: npx-based examples can execute packages from the package registry. <br>
Mitigation: Run npx examples only in environments where the referenced packages and registry source are trusted. <br>
Risk: Public image exports can unintentionally expose GPS, camera, personal, or rights metadata. <br>
Mitigation: Make metadata decisions deliberately and strip or preserve fields according to the delivery context before publishing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/image) <br>
- [Image Skill Homepage](https://clawic.com/skills/image) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; command examples may reference local image files and external package runners.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
