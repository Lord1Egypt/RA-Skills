## Description:

Trello (trello.com). Use this skill for ANY Trello request — reading, creating, updating, and deleting data. Whenever a task involves Trello, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Trello can ask the agent to find boards, cards, members, labels, comments, and checklists, or to create and update Trello content through their connected account. The skill requires confirmation of exact effects before write actions and explicit approval before destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path may execute a downloaded script with local permissions; the script contents were not determined, and the security review was partial.

Mitigation: Use an existing oo CLI when available. Before installing, review the installer and resolve the incomplete security review.

Risk: Write and destructive actions change Trello content.

Mitigation: Confirm the exact payload and effect before write actions, and obtain explicit approval for destructive actions.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Trello](https://trello.com)
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read Trello data or propose changes; write and destructive actions require user confirmation as described in the skill.]

## Skill Version(s):

1.0.7 (source: artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
