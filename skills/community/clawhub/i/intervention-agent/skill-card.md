## Description:

AI collaboration assistant that helps agents learn from mistakes and user corrections through a mistake journal, human intervention points, friction detection, and collaboration memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldcharding](https://clawhub.ai/user/goldcharding)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to make agent collaboration more adaptive by tracking corrections, surfacing progress, pausing at decision points, and remembering collaboration preferences across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save collaboration preferences, corrections, and friction patterns persistently.

Mitigation: Avoid including sensitive personal, business, or credential details in correction examples unless the user understands where OpenClaw memory is stored and how to delete it.

Risk: Preference learning could apply an incorrect correction or workflow preference in later sessions.

Mitigation: Require confirmation before important learnings take effect and let the user remain the final decision-maker.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/goldcharding/skills/intervention-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with examples, workflow steps, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include status messages, confirmation prompts, remembered preference summaries, and mistake-journal entries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
