## Description: <br>
Learn user preferences from conversations and personalize responses automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fliellerjulian](https://clawhub.ai/user/fliellerjulian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agent operators use pref0 to track conversation-derived preferences, retrieve a user's preference profile before responding, and reset stored preferences when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation-derived data and persistent user identifiers are sent to and stored by a third-party service. <br>
Mitigation: Install only when that data sharing is acceptable, use opaque internal user IDs, and avoid tracking sensitive conversations. <br>
Risk: The returned preference prompt can influence future agent instructions. <br>
Mitigation: Prefer structured preferences or review the prompt before use, and do not allow preferences to override safety or policy requirements. <br>
Risk: Stored preferences may need to be reset or removed for a user. <br>
Mitigation: Use the delete profile endpoint when a user asks to reset or remove stored preferences. <br>


## Reference(s): <br>
- [pref0 ClawHub listing](https://clawhub.ai/fliellerjulian/pref0) <br>
- [pref0 API](https://api.pref0.com) <br>
- [pref0 signup](https://pref0.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Text] <br>
**Output Format:** [Markdown with HTTP endpoint examples, shell commands, and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PREF0_API_KEY; sends conversation history and persistent user identifiers to the pref0 API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
