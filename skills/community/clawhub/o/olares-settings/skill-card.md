## Description: <br>
Olares Settings (olares-cli settings) helps an agent read and mutate Olares Settings UI surfaces from the command line for the active Olares ID, including users, apps, integrations, VPN, backup, restore, appearance, search, network, GPU, video, and advanced settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olares](https://clawhub.ai/user/olares) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, and administrators use this skill to ask an agent for Olares settings guidance and command proposals for inspecting or changing per-Olares-ID configuration. It is most relevant when managing Olares users, app settings, integration accounts, VPN access, backup state, search indexing, appearance, or related Settings UI surfaces through olares-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that change Olares settings, including user deletion, app environment or domain changes, VPN ACL or SSH changes, integration account updates, and backup password rotation. <br>
Mitigation: Review proposed commands before approving writes, and verify the target user, app, integration, VPN rule, or backup plan before execution. <br>
Risk: Access keys, SSO tokens, generated passwords, backup passwords, and TLS private keys can be exposed in chat transcripts or shell history. <br>
Mitigation: Keep secrets out of chat and command history; use environment variables, stdin, TTY prompts, or secret managers where supported. <br>


## Reference(s): <br>
- [Olares Settings documentation](https://docs.olares.com/manual/olares/settings/) <br>
- [ClawHub skill page](https://clawhub.ai/olares/olares-settings) <br>
- [settings apps reference](references/olares-settings-apps.md) <br>
- [settings backup reference](references/olares-settings-backup.md) <br>
- [settings integration reference](references/olares-settings-integration.md) <br>
- [settings users reference](references/olares-settings-users.md) <br>
- [settings vpn reference](references/olares-settings-vpn.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command proposals may include table or JSON output modes from olares-cli settings.] <br>

## Skill Version(s): <br>
4.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
