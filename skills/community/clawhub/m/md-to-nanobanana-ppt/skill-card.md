## Description: <br>
Converts Markdown analysis reports into presentation decks by proposing color schemes, splitting content into up to 20 slides, generating NanoBanana image prompts and images, and packaging the result as a PPTX for Feishu or QQ email delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunni123](https://clawhub.ai/user/yunni123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Report authors and agents use this skill to turn Markdown analysis reports into visual PPT decks with selected color schemes, generated slide images, progress updates, and final delivery through Feishu or QQ email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown report contents may be used in image-generation prompts and handled by external delivery channels. <br>
Mitigation: Review report sensitivity before use and avoid processing confidential content unless those services are approved for the data. <br>
Risk: Large PPT files are delivered by QQ email after the user provides a recipient address. <br>
Mitigation: Ask the user for an explicit recipient address and verify it before sending attachments. <br>
Risk: Generated images and PPT files are saved to a local output directory. <br>
Mitigation: Remove generated local outputs after delivery when the source report or deck contains sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yunni123/md-to-nanobanana-ppt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown progress updates, PPTX presentation files, and PNG slide images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves outputs under ~/.openclaw/media/ai-choise/md-to-nanobanana-ppt/, limits decks to 20 slides, and routes delivery based on a 30 MB file-size threshold.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
