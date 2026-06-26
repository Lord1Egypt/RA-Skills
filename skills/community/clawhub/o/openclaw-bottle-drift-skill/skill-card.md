## Description: <br>
Bottle Drift lets OpenClaw users run a local relay with a web dashboard and CLI for sending short messages to online channel subscribers and collecting one-time replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw node operators and community builders use this skill to host a lightweight bottle-drift message relay where online subscribed users can receive short notes and reply once through a dashboard, CLI, or reply link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The relay exposes inbox, reply-link, presence, and callback data without real authentication when deployed beyond localhost or a trusted private network. <br>
Mitigation: Use it only for local testing or trusted private networks unless authentication, authenticated inbox access controls, and private handling of reply tokens and callback URLs are added. <br>
Risk: The current identity model is based on user_id values and browser-local state rather than platform identity. <br>
Mitigation: Connect the relay to a real identity provider before public deployment and restrict each user's inbox and reply operations to that authenticated user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/openclaw-bottle-drift-skill) <br>
- [README](README.md) <br>
- [Message schema](resources/message_schema.json) <br>
- [Smoke test](tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with CLI commands, HTTP endpoint behavior, dashboard output, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and uses local HTTP plus SQLite with bundled dashboard resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
