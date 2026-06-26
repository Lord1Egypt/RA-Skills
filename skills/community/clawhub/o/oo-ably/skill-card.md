## Description: <br>
Ably helps agents operate a connected Ably account through the OOMOL oo CLI connector for channel metadata, presence, history, usage stats, push subscriptions, and message publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Ably channels, presence, message history, usage stats, push subscriptions, and message publishing through a connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive Ably actions can alter channel state, publish messages, or delete push notification subscriptions. <br>
Mitigation: Confirm the exact payload, target channel or subscription, and intended effect with the user before write actions, and require explicit approval before destructive actions. <br>
Risk: The skill requires a connected Ably account and sensitive credentials. <br>
Mitigation: Use OOMOL's server-side credential injection, avoid exposing raw tokens, and only run authentication or connection setup after an auth or connection failure. <br>
Risk: Connector action schemas may determine required inputs at execution time. <br>
Mitigation: Inspect the live action schema with the oo CLI before constructing payloads. <br>


## Reference(s): <br>
- [Ably homepage](https://ably.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub Ably skill page](https://clawhub.ai/oomol/oo-ably) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Ably connector action names, JSON payloads, execution IDs, and confirmation prompts for write or destructive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
