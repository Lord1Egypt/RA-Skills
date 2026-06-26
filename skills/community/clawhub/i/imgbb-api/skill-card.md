## Description: <br>
Upload images to ImgBB via local file, URL, or base64 and get shareable direct links, supporting batch uploads and optional expiration settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KeXu9](https://clawhub.ai/user/KeXu9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to upload selected local, remote, or base64-encoded images to ImgBB and return shareable image URLs. It is useful for converting image assets into externally hosted links for sharing or downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images are sent to an external image hosting service and may become externally accessible. <br>
Mitigation: Use the skill only for images intended for external hosting, and avoid private, regulated, internal, or sensitive content unless that exposure is acceptable. <br>
Risk: The skill can store an ImgBB API key in ~/.imgbb_api_key when the saved-key option is used. <br>
Mitigation: Prefer the IMGBB_API_KEY environment variable, or ensure ~/.imgbb_api_key is readable only by the current account. <br>


## Reference(s): <br>
- [ImgBB API](https://api.imgbb.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/KeXu9/imgbb-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON upload results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns direct image URLs, viewer URLs, thumbnail URLs when available, or upload error messages.] <br>

## Skill Version(s): <br>
1.1.2 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
