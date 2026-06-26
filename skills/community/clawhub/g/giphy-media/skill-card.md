## Description: <br>
Search GIFs, stickers, emojis, trending media, and upload assets to GIPHY via the GIPHY API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to find GIPHY media, browse trending content, translate phrases into matching GIFs or stickers, retrieve media by ID, and upload GIF or video assets after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on ClawLink to manage credentials and proxy authenticated GIPHY requests. <br>
Mitigation: Connect only an account suitable for GIPHY searches and uploads, and verify the GIPHY connection through ClawLink before use. <br>
Risk: Uploaded GIF or video assets may become public or searchable through GIPHY. <br>
Mitigation: Preview upload details and obtain explicit user confirmation before any upload. <br>
Risk: Uploaded media may violate third-party rights or GIPHY terms if the user does not have permission to share it. <br>
Mitigation: Confirm that the user has rights to upload the media and review the upload target before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/giphy-media) <br>
- [GIPHY API Documentation](https://developers.giphy.com/docs/api/) <br>
- [GIPHY Developers](https://developers.giphy.com/) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=giphy-media) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate authenticated GIPHY searches, lookups, trending queries, translation requests, and confirmed uploads through ClawLink tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
