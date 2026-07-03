## Description: <br>
Stateless Go CLI for agents to search files, retrieve itineraries, upload attachments, and manage documents in the Lynx Reservations travel agency system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredguile](https://clawhub.ai/user/fredguile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel operations agents and developers use this skill to run standalone Lynx CLI commands for reservation file lookup, itinerary retrieval, attachment upload, and document updates with valid Lynx credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify live Lynx reservation documents and upload selected local files to Lynx. <br>
Mitigation: Review file search, upload, and document-save commands carefully before running them against production reservation records. <br>
Risk: Debug mode can leave sensitive reservation data in temporary output. <br>
Mitigation: Avoid enabling LYNX_DEBUG unless temporary output can be protected and cleaned after use. <br>
Risk: Lynx credentials are sensitive and are required for use. <br>
Mitigation: Do not paste raw LYNX_* values into logs, prompts, or support chats. <br>


## Reference(s): <br>
- [ClawHub Lynx Skill](https://clawhub.ai/fredguile/lynx-skill) <br>
- [Lynx Reservations](https://www.lynx-reservations.com/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require valid LYNX_USERNAME, LYNX_PASSWORD, and LYNX_COMPANY_CODE credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
