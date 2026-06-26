## Description: <br>
Use when users need SMS code login, session creation, and HTML message exchange via /session/login and /session/message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayleethu](https://clawhub.ai/user/rayleethu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request SMS verification, create or reuse login sessions, and send HTML-backed chat messages to the documented zhibianai.com service. It is intended for workflows that need session-based beauty consultation message exchange. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends SMS login details and HTML content to the documented zhibianai.com service. <br>
Mitigation: Install and run it only when the publisher and service destination are trusted, and ask the user before transmitting login data or message content. <br>
Risk: The skill uses CLAWHUB_SKILL_TOKEN and can persist user_id and session_id in .session.json. <br>
Mitigation: Treat the token and session file as sensitive secrets, restrict file permissions, and delete the session file after use when persistence is not needed. <br>
Risk: HTML inputs and outputs can carry unsafe markup if used without filtering. <br>
Mitigation: Apply an HTML allowlist and block active or embedded content before sending or rendering HTML. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rayleethu/pengleni-login-session-html-bridge) <br>
- [zhibianai.com service root](https://www.zhibianai.com) <br>
- [zhibianai.com ClawHub API base](https://www.zhibianai.com/api/v1/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON, HTML, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist user_id and session_id in .session.json; message responses may include answer_text and answer_html.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
