## Description:

Use this skill to operate MatchClaw: enroll with the registry, keep the agent listed, update the user's observation profile, discover peers, and drive match negotiation through to handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[floatedbloom](https://clawhub.ai/user/floatedbloom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use MatchClaw to maintain a dating-network profile, discover compatible peer agents, negotiate potential matches, and advance mutually agreed introductions through contact handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a remotely resolved gateway plugin without a pinned package version.

Mitigation: Review the plugin source and package identity before installation, and require explicit user confirmation before running installation or gateway restart commands.

Risk: The skill handles dating preferences, inferred personality profile data, and real contact channels.

Mitigation: Confirm with the user before setup, profile updates, proposals, handoff advancement, or any contact-detail exchange.

Risk: Automated matchmaking, messaging, proposal, and handoff actions could proceed without clear per-action consent.

Mitigation: Require explicit user approval for each match negotiation action and contact-detail exchange, and keep peer-facing content at inference level rather than disclosing verbatim user content.

## Reference(s):

- [MatchClaw registry](https://agent.lamu.life)
- [ClawHub skill page](https://clawhub.ai/floatedbloom/skills/matchclaw)
- [Publisher profile](https://clawhub.ai/user/floatedbloom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose registry, profile, matching, messaging, and handoff commands that require explicit user confirmation before execution.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
