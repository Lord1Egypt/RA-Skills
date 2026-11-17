## Description:

MindMatch helps an agent find compatible people by building psychological profiles and assessing romantic, business, friendship, or custom matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivankoriako](https://clawhub.ai/user/ivankoriako)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent to identify compatible romantic partners, business co-founders, friends, or custom matches from psychological compatibility signals. The skill is described as coming soon, with the profile builder and matching engine still in development.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes psychological profiling from conversation history and remote matching, while the server evidence says its privacy claims and controls are under-scoped.

Mitigation: Require explicit user opt-in, explain what conversation history is read, show the derived profile for review before upload, and disclose where profile data is sent and retained.

Risk: Users could disclose private conversation history or sensitive inferred traits to a remote matching service.

Mitigation: Do not use the skill with private conversation history unless the missing disclosure, consent, profile review, retention, and remote-transfer controls are added or the user accepts that disclosure.

## Reference(s):

- [Mindmatch ClawHub skill page](https://clawhub.ai/ivankoriako/skills/mindmatch)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text guidance and compatibility analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve sensitive psychological profile data and remote matching when the service is implemented.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
