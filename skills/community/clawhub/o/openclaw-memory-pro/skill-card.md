## Description:

Enhanced AI memory system with vector storage, document-level MSA, a knowledge graph, collision workflows, executable skills, and closed-loop skill evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fluffyaicode](https://clawhub.ai/user/fluffyaicode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual users use this skill to install and operate a persistent AI memory system for storing notes, recalling evidence, surfacing knowledge-graph relationships, generating briefings, and evolving local skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may store sensitive conversations, notes, and high-importance content over time.

Mitigation: Use an isolated environment, avoid storing secrets or regulated data unless explicitly approved, and review retention/export behavior before use.

Risk: The skill can access LLM credentials through environment variables or shared OpenClaw auth profiles.

Mitigation: Use dedicated low-quota API keys, restrict credential scope, and avoid shared credential fallback until the implementation has been reviewed.

Risk: Mutable source installs and scheduled background work can change or run behavior outside an immediate interactive request.

Mitigation: Pin the repository to a reviewed commit, inspect scheduled tasks before enabling the server, and monitor generated briefings, collision rounds, and exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fluffyaicode/skills/openclaw-memory-pro)
- [Source repository listed by artifact](https://github.com/FluffyAIcode/openclaw-memory-pro-system)
- [Setup guide](setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include memory recall results, knowledge-graph relationships, evidence snippets, briefing content, skill utility information, and setup guidance.]

## Skill Version(s):

0.0.7 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
