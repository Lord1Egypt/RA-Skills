## Description: <br>
Getnote helps an agent save, search, retrieve, organize, and manage a user's Get笔记 notes and knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to connect an agent to their Get笔记 account for personal note capture, semantic recall, note detail retrieval, tagging, knowledge-base organization, and image or link note workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload user content and access private notes through Get笔记. <br>
Mitigation: Install it only for accounts where agent-managed Get笔记 access is intended, and review save, search, and retrieval requests before use. <br>
Risk: Long-lived credentials may persist locally after OAuth authorization. <br>
Mitigation: Use the official Get笔记 authorization page, keep credentials out of chat, and revoke keys when access is no longer needed. <br>
Risk: Shared or group environments may expose private note operations to the wrong user. <br>
Mitigation: Configure GETNOTE_OWNER_ID in shared contexts so the agent can restrict note operations to the intended owner. <br>
Risk: Links, images, OCR text, searches, and note contents may be sent to Get笔记. <br>
Mitigation: Avoid using the skill with content that should not be processed by the Get笔记 service. <br>


## Reference(s): <br>
- [Get笔记 homepage](https://biji.com) <br>
- [Get笔记 open platform](https://www.biji.com/openapi) <br>
- [Get笔记 API details](references/api-details.md) <br>
- [ClawHub release page](https://clawhub.ai/lovefromio/lovefromio-getnote) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown or text responses with JSON API payloads and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Get笔记 OAuth/API credentials and may send links, images, OCR text, searches, and note contents to Get笔记.] <br>

## Skill Version(s): <br>
1.7.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
