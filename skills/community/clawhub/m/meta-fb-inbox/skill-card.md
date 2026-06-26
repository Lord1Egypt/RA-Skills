## Description: <br>
Check Facebook page inbox messages via Meta Business Suite browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PicSeeInc](https://clawhub.ai/user/PicSeeInc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Customer support and social media operations teams use this skill to inspect Facebook Page inboxes, review unread messages, reply to customers, manage conversation labels and notes, and retrieve direct conversation URLs through Meta Business Suite browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a logged-in Meta Business inbox and may read or modify customer conversations, labels, and internal notes. <br>
Mitigation: Use a dedicated low-privilege Meta account where possible and review replies, label changes, and note changes before submission. <br>
Risk: Conversation URLs and extracted message content can expose customer data if stored or shared unnecessarily. <br>
Mitigation: Avoid saving conversation URLs unless needed and treat any exported conversation details as sensitive customer information. <br>
Risk: Downloaded message images are saved under the user's Downloads directory and may contain untrusted customer-provided content. <br>
Mitigation: Treat downloaded images as sensitive untrusted files and open or share them only after appropriate review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PicSeeInc/meta-fb-inbox) <br>
- [Meta Business Suite](https://business.facebook.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with browser actions, shell commands, JSON configuration examples, and extracted conversation summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output customer names, message previews, read or unread status, conversation URLs, labels, notes, and local file paths for downloaded images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
