## Description: <br>
Telegram Mini App Canvas renders agent-generated HTML, markdown, text, or A2UI content in a Telegram Mini App, with a JWT-gated browser terminal and an optional OpenClaw Control UI proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clvv](https://clawhub.ai/user/clvv) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this server skill to push live agent-generated UI content into Telegram and optionally access a protected terminal or OpenClaw Control UI from approved Telegram users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pushed web content can execute scripts inside the Telegram Mini App context. <br>
Mitigation: Prefer markdown or text payloads over untrusted HTML and only allow trusted agents or operators to push content. <br>
Risk: The browser terminal grants shell access on the machine running the server to approved Telegram users. <br>
Mitigation: Run the server as a non-root user on an isolated host or container and keep ALLOWED_USER_IDS limited to users trusted with shell access. <br>
Risk: Public tunnels can make loopback-origin checks unreliable for push and clear endpoints. <br>
Mitigation: Use a strong PUSH_TOKEN and keep it secret; the server refuses startup when PUSH_TOKEN is missing. <br>
Risk: The optional OpenClaw Control UI proxy can expose local control functionality through the Mini App. <br>
Mitigation: Leave ENABLE_OPENCLAW_PROXY disabled unless needed and protect any enabled Control UI path with strong authentication and narrow user access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clvv/openclaw-tg-canvas) <br>
- [Publisher profile](https://clawhub.ai/user/clvv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML/text payloads, JSON API responses, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, cloudflared, Telegram bot configuration, BOT_TOKEN, ALLOWED_USER_IDS, JWT_SECRET, MINIAPP_URL, and PUSH_TOKEN.] <br>

## Skill Version(s): <br>
0.2.6 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
