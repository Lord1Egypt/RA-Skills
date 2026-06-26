## Description: <br>
Gates persona sharing behind explicit Telegram owner approval and connects to persona-service for external chatbots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kanishkaRandunu](https://clawhub.ai/user/kanishkaRandunu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to require Telegram owner approval before sharing local persona, profile, identity, writing style, or system-prompt/personality details. When configured with persona-service, it can poll for external chatbot persona requests and return approved results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional service mode can start an unsupervised background persona-client that handles secrets and sends approved persona data to an external service. <br>
Mitigation: Use this mode only with a trusted HTTPS persona-service, configure a shared secret, and supervise or manually run the persona-client so it can be stopped when needed. <br>
Risk: Misconfigured persona paths could expose the wrong local persona file. <br>
Mitigation: Set PERSONA_PATH and ALLOWED_PERSONA_PATH to the exact same intended file and verify the path before enabling the skill. <br>
Risk: Telegram bot tokens, chat IDs, and persona-service shared secrets can be exposed through terminals, screenshots, or logs. <br>
Mitigation: Use a dedicated Telegram bot for approval and rotate any Telegram or service secrets that may have been pasted into terminals, screenshots, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kanishkaRandunu/persona-consent-telegram-hub) <br>
- [README](README.md) <br>
- [End-to-end test](docs/E2E-TEST.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns persona text only after approval; denial, timeout, or errors return a refusal JSON or the exact refusal text.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
