## Description:

Anticipates needs, keeps work moving, and improves through use so the agent gets more proactive over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panwang813](https://clawhub.ai/user/panwang813)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add proactive operating behavior, local follow-through state, boundary-aware suggestions, and recovery patterns to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores local cross-session proactivity notes in ~/proactivity/, which may include sensitive personal or project context if users place it there.

Mitigation: Keep secrets and sensitive personal data out of proactivity files, and periodically review local notes for data that should not persist.

Risk: Optional AGENTS, TOOLS, SOUL, and HEARTBEAT snippets can affect future agent behavior if approved without review.

Mitigation: Review the exact proposed snippets before approving workspace integration, and require explicit approval for edits outside ~/proactivity/.

Risk: Proactive suggestions or follow-up actions may be unwanted if they exceed the user's boundaries.

Mitigation: Use the documented boundary ladder and ask before external communication, spending, deletion, scheduling, commitments, or workspace edits.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/panwang813/skills/proactivity-bak)
- [Skill homepage](https://clawic.com/skills/proactivity)
- [Publisher profile](https://clawhub.ai/user/panwang813)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local proactivity state under ~/proactivity/ when the user chooses to use the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
