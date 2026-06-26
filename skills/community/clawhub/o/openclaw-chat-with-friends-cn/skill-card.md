## Description: <br>
Guides users through setting up a Telegram channel so multiple OpenClaw bots can chat with each other and with friends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moon-frost](https://clawhub.ai/user/Moon-frost) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to create or join a Telegram channel, add multiple OpenClaw bots as channel administrators, connect the channel to OpenClaw, and persist channel behavior rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disabling Telegram bot privacy mode and adding bots as channel administrators can expose channel messages to the involved bots. <br>
Mitigation: Use a private channel with consenting participants, grant only the minimum Telegram permissions needed, and avoid sensitive conversations in the channel. <br>
Risk: Using third-party Chat ID helper bots can expose forwarded channel messages or identifiers. <br>
Mitigation: Use non-sensitive test messages when relying on helper bots, and remove stale channel details or unneeded bot administrator permissions after setup. <br>
Risk: Loose channel rules can cause bots to reply to each other repeatedly. <br>
Mitigation: Configure name prefixes, reply triggers, cooldowns, and persistent AGENTS.md rules before sustained use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Moon-frost/openclaw-chat-with-friends-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown setup guidance with checklists, troubleshooting notes, and example channel-rule configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces conversational setup steps for Telegram, OpenClaw channel binding, and AGENTS.md rule persistence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
