## Description: <br>
Operate Sendbird through an OOMOL-connected account for reading, creating, updating, and deleting Sendbird data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Sendbird group channels, users, messages, members, bans, mutes, and session tokens through the oo CLI. It is intended for authenticated Sendbird administration where reads can be run directly and state-changing actions require confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run authenticated Sendbird write and destructive actions that affect channels, users, messages, membership, bans, mutes, and session tokens. <br>
Mitigation: Confirm the exact target, payload, and expected effect before any write action, and require explicit approval before destructive actions. <br>
Risk: Incorrect payloads or stale assumptions about a Sendbird action can change the wrong resource or fail unexpectedly. <br>
Mitigation: Fetch the live action schema with `oo connector schema` before constructing a payload. <br>
Risk: The skill requires an authenticated OOMOL connection to Sendbird and may expose operational access through the connected account. <br>
Mitigation: Use only authorized accounts, avoid handling raw credentials directly, and reconnect or adjust scopes only when an auth or connection error requires it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-sendbird) <br>
- [Sendbird Homepage](https://sendbird.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL Sendbird Connection](https://console.oomol.com/app-connections?provider=sendbird) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include oo CLI commands, Sendbird action names, schema inspection steps, and confirmation prompts for write or destructive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
