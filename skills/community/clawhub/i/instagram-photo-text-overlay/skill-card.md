## Description: <br>
Overlay text on photos for Instagram posts by generating portrait (4:5) images with gradient overlays, titles, and optional numbered lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psyduckler](https://clawhub.ai/user/psyduckler) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, social media managers, and developers use this skill to turn selected photos into Instagram-ready portrait images with readable titles, list items, quotes, watermarks, and accent colors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running dependencies from an untrusted source could introduce supply-chain risk. <br>
Mitigation: Install Pillow only from a trusted package source and run the script from the skill directory. <br>
Risk: The output path may overwrite an existing file. <br>
Mitigation: Choose a deliberate output filename that does not point to an important existing file. <br>
Risk: Input photos may contain private or sensitive content. <br>
Mitigation: Use photos that are intended for local processing and sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/psyduckler/instagram-photo-text-overlay) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [JPEG image files plus Markdown or plain-text command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates 4:5 portrait images; requires local Python 3 and Pillow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
