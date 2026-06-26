## Description: <br>
Publish, edit, or configure notes on Mowen via its Open API, including rich text, images, note settings, and privacy controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacobluo](https://clawhub.ai/user/jacobluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Mowen notes, update API-created notes, and modify note privacy or sharing settings from structured note content. It is useful when a workflow needs to publish social-media-style notes with rich text and images through Mowen. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected note text and local or remote images are sent to Mowen. <br>
Mitigation: Use the skill only when Mowen is the intended destination and avoid confidential content unless Mowen's privacy and retention practices are acceptable. <br>
Risk: Editing a note replaces the full note body. <br>
Mitigation: Fetch or back up the existing note before editing, and keep the noteId returned by creation for follow-up edits or settings changes. <br>
Risk: Auto-publish and privacy settings can expose note content beyond the intended audience. <br>
Mitigation: Confirm autoPublish and privacyType settings before running create or settings actions. <br>


## Reference(s): <br>
- [Mowen Open API reference](artifact/references/mowen_api.md) <br>
- [Mowen Open API endpoint](https://open.mowen.cn) <br>
- [ClawHub skill page](https://clawhub.ai/jacobluo/mowenskill-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads; the helper script returns JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and a MOWEN_API_KEY environment variable or --api-key argument.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
