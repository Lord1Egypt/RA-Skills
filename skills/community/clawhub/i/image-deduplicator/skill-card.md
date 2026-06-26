## Description: <br>
Detect and remove exact or visually similar duplicate images in local folders using MD5 and perceptual hashing with configurable actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mingo-318](https://clawhub.ai/user/Mingo-318) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, data practitioners, and users managing image folders use this skill to scan local directories for exact or visually similar duplicate images and choose whether to list, move, or delete duplicate files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Duplicate cleanup can delete or move local files when destructive actions are selected. <br>
Mitigation: Run list mode first, review the files that would be affected, back up important folders, and prefer move mode when unsure. <br>
Risk: Image processing depends on local Pillow and imagehash installations. <br>
Mitigation: Install trusted, pinned versions of dependencies before running scans in important folders. <br>


## Reference(s): <br>
- [Image Deduplicator on ClawHub](https://clawhub.ai/Mingo-318/image-deduplicator) <br>
- [Publisher profile](https://clawhub.ai/user/Mingo-318) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file listing, move, or delete workflows for duplicate image cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
