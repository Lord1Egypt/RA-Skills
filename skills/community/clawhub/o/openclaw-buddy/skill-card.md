## Description: <br>
Generate a unique deterministic virtual pet buddy from a user identifier, including species, rarity, stats, cosmetics, personality text, and ASCII art. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylinr](https://clawhub.ai/user/kylinr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and community agents use this skill to generate a deterministic virtual pet card for a user from a stable platform ID or custom seed. It is useful for chat-based identity, engagement, and lightweight personalization workflows where repeatable results matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a stable platform user ID, such as a Feishu open_id or Discord/Telegram ID, as the deterministic seed. <br>
Mitigation: Use a custom seed instead of a private identifier when privacy matters, and avoid generating buddies for other people without consent. <br>


## Reference(s): <br>
- [OpenClaw Buddy Skill Page](https://clawhub.ai/kylinr/openclaw-buddy) <br>
- [Publisher Profile](https://clawhub.ai/user/kylinr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown-ready text card on stdout with JSON data on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic output for the same seed; bilingual Chinese and English labels; ASCII art is best displayed in monospace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
