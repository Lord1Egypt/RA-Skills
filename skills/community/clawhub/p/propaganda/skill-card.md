## Description:

Detects and analyzes propaganda, influence operations, and narrative manipulation in news articles, social media posts, and media narratives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xdeadcafe](https://clawhub.ai/user/0xdeadcafe)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, analysts, and researchers use this skill to deconstruct articles, social posts, press releases, transcripts, and official narratives by separating claims, framing, omissions, and evidence-supported conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes narrative structure but does not externally verify facts.

Mitigation: Treat results as analytical guidance and verify important factual claims against trusted sources before acting on them.

Risk: The optional curl shortcut fetches remote content before passing it to an agent.

Mitigation: Use the shortcut only for sources the user is comfortable sharing with the agent, and avoid sending sensitive source text.

## Reference(s):

- [Server-resolved source repository](https://github.com/0xdeadcafe/Propaganda)
- [ClawHub skill page](https://clawhub.ai/0xdeadcafe/skills/propaganda)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports FLASH, STANDARD, and DEEP response modes with output length varying by source text length and user request.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
