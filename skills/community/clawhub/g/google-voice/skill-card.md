## Description: <br>
Google Voice web-client automation and MCP integration from HAR captures for listing, reading, exporting, and sending SMS; starting calls; injecting approved TTS or local audio; recording call audio; and configuring the bundled HAR-derived MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations agents use this skill to inspect Google Voice HAR-derived endpoints, manage authorized SMS records, and perform explicitly approved outbound messaging or calling through a logged-in Google Voice session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose or act on private Google Voice messages, calls, recordings, and raw authenticated API calls. <br>
Mitigation: Install only in a trusted local workspace, use a dedicated account or isolated browser profile where possible, and confirm exact recipients, message text, phone numbers, and recording consent before use. <br>
Risk: HAR files, SMS exports, cookies, API keys, OAuth tokens, transcripts, and recordings are sensitive secrets. <br>
Mitigation: Prefer browser authentication, avoid gv_raw_call, gws mode, GV_COOKIE, GV_AUTHORIZATION, and cookie exports unless specifically needed, and keep all generated records and credentials out of prompts and committed files. <br>


## Reference(s): <br>
- [Google Voice Skill Page](https://clawhub.ai/earlvanze/google-voice) <br>
- [Google Voice HAR notes](references/har-endpoints.md) <br>
- [Google Voice call HAR notes](references/call-har-endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and generated configuration or code snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON or Markdown exports for SMS records and can invoke local MCP or browser automation when explicitly authorized.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
