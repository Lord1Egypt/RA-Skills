## Description: <br>
Remove image watermarks with the Nowatermark.info API, request polling, request_id resume, and public image URL validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxcoder11](https://clawhub.ai/user/maxcoder11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw agents and their operators use this skill to submit authorized public image URLs to Nowatermark.info, poll for completion, resume existing request IDs, and return the cleaned image URL or failure details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted public image URLs and resulting processing data are sent to Nowatermark.info. <br>
Mitigation: Use the skill only for images the user is authorized to edit, and avoid confidential, regulated, private, or legally restricted images. <br>
Risk: The skill requires the sensitive NOWATERMARK_API_KEY credential. <br>
Mitigation: Provide the key through environment or skill settings, keep it out of logs and replies, and rotate it if exposure is suspected. <br>
Risk: Removing a watermark without permission can violate ownership or usage rights. <br>
Mitigation: Confirm the user is allowed to edit the image before submitting it when ownership or permission is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maxcoder11/image-watermark-remover) <br>
- [Nowatermark.info](https://nowatermark.info) <br>
- [API reference](artifact/references/api.md) <br>
- [Setup](artifact/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOWATERMARK_API_KEY and either one direct public image URL or an existing request_id; completed jobs return a cleaned image URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, frontmatter, and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
