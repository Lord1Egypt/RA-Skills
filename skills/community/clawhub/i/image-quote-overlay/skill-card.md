## Description: <br>
Creates social-media quote images by selecting a random JPG from a configured photo folder, applying a dark gradient overlay, and adding quote, author, role, and contact text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quoc-modoro](https://clawhub.ai/user/quoc-modoro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and automation agents use this skill to generate 1200x630 quote images for LinkedIn, X, Facebook, and WordPress posts from a configured image folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can select random personal photos from PICS_DIR, which may expose private or unintended images in generated outputs. <br>
Mitigation: Use a dedicated non-sensitive JPG folder for PICS_DIR and review generated images before sharing or publishing them. <br>
Risk: Generated image paths can be passed to other skills or posting workflows, which may share files beyond the local workspace. <br>
Mitigation: Write outputs only to an approved directory, share generated files intentionally, and delete generated images when no longer needed. <br>
Risk: The shell script depends on local ImageMagick and font paths, so execution may fail or produce inconsistent images on differently configured machines. <br>
Mitigation: Confirm ImageMagick, required fonts, PICS_DIR, and output permissions before using the skill in an automated workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/quoc-modoro/image-quote-overlay) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bash, ImageMagick, configured fonts, and at least one JPG image in PICS_DIR.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
