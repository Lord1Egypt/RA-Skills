## Description: <br>
Adopt and care for a MagicHaqi virtual pet with a user's consent by logging into the browser game, reading pet state, and sending supported care, chat, adoption, and sharing commands through the page's hidden agent interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paraengine](https://clawhub.ai/user/paraengine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to adopt, monitor, feed, clean, play with, talk to, and share a MagicHaqi virtual pet through the live browser game. The skill is intended for consent-driven pet care sessions where the agent reads game state before acting and asks before adoption or in-game spending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require the agent to handle a KeepWork password or login token. <br>
Mitigation: Prefer user-completed browser login when possible, verify the MagicHaqi host before using a token, do not reuse a high-value password, and never print or log credentials. <br>
Risk: Adoption binds an agent owner and buying items spends in-game coins. <br>
Mitigation: Require explicit human approval before adoption or any purchase. <br>
Risk: Care, chat, and navigation commands change game state through the live page. <br>
Mitigation: Read machine-readable state before acting, pace commands, re-read state after each write, and use screenshots when visual confirmation is needed. <br>


## Reference(s): <br>
- [MagicHaqi Pet Master on ClawHub](https://clawhub.ai/paraengine/pet-master) <br>
- [MagicHaqi Agent Commands](artifact/commands.md) <br>
- [MagicHaqi Agent Integration](artifact/integration.md) <br>
- [KeepWork login API endpoint](https://api.keepwork.com/core/v0/users/login) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON commands, Browser actions, Configuration] <br>
**Output Format:** [Markdown instructions with HTTP examples, URL parameters, DOM selectors, and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be sent after reading state, then verified by refreshed state or screenshot; adoption and in-game spending require explicit user consent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
