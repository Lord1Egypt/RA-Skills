## Description: <br>
保利威直播 helps agents use the published polyv-live-cli npm package to query and manage Polyv live-streaming channels, stream state, products, coupons, playback, documents, sessions, chat, interactive tools, viewers, access controls, platform settings, player configuration, AI features, monitoring, scene setup, and statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polyv](https://clawhub.ai/user/polyv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Polyv administrators and developers use this skill to route natural-language live-stream operations to the current polyv-live-cli command surface. It supports operational tasks such as checking channels, configuring streams and playback, managing viewer access, exporting reports, and administering live interaction features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad access to production live-stream administration, including channel, playback, interaction, access-control, and platform settings. <br>
Mitigation: Install only for authorized Polyv administrators, use test accounts first, and confirm the active account before any write or production-impacting command. <br>
Risk: Commands using --force, --global, --clear, callback changes, or platform-wide setting updates can have high-impact or account-wide effects. <br>
Mitigation: Require human review of the exact target and impact before using these options or changing callback and platform-wide settings. <br>
Risk: Exports and query results can include sensitive viewer, donor, whitelist, check-in, and statistics data. <br>
Mitigation: Treat exported files and command output as sensitive data and limit access, storage, and sharing to authorized users. <br>
Risk: Credential exposure can occur if AppSecret or account credentials are placed directly on command lines or in shared materials. <br>
Mitigation: Prefer stored account configuration or protected environment variables and avoid echoing or documenting secrets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/polyv/skills/polyv-live-cli) <br>
- [Polyv Website](https://www.polyv.net/) <br>
- [Polyv Live API Documentation](https://help.polyv.net/#/live/api/) <br>
- [Skill Instructions](SKILL.md) <br>
- [Task Routing Reference](references/task-routing.md) <br>
- [Command Index](references/command-index.md) <br>
- [Authentication Reference](references/authentication.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to verify the npm-published CLI help before business commands and to prefer JSON output for extraction, comparison, reports, and scripts.] <br>

## Skill Version(s): <br>
1.0.8 (source: evidence.release.version; release notes reference polyv-live-cli@1.2.31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
