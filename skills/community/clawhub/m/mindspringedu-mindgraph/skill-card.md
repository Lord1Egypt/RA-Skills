## Description:

MindGraph diagrams from a topic plus diagram type (8 Thinking Maps, mind map, or concept map), or precise node text edits via PATCH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycosa9527](https://clawhub.ai/user/lycosa9527)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate MindGraph diagrams from a topic and diagram type, then save, render, and edit diagrams through the MindGraph HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a MindGraph API token and account value, and unsafe handling could expose credentials.

Mitigation: Configure credentials through a secure per-skill environment or secret store, avoid pasting live credentials into chat, and regenerate the token if credentials were exposed.

Risk: The security verdict is suspicious because setup guidance includes unsafe credential-handling paths.

Mitigation: Review the skill before installing and remove affected transcripts where possible if live credentials were shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycosa9527/skills/mindspringedu-mindgraph)
- [Publisher profile](https://clawhub.ai/user/lycosa9527)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [API calls, JSON, Markdown, Configuration guidance]

**Output Format:** [Markdown guidance with JSON request bodies, HTTP endpoint instructions, and signed PNG URL handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINDGRAPH_BASE_URL, MINDGRAPH_ACCOUNT, and MINDGRAPH_TOKEN; diagram PNG links are signed and time-limited.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
