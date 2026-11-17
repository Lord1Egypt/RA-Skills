## Description:

Analyze text files for word count, character count, line count, sentence count, reading time, speaking time, readability scores (Flesch Reading Ease, Flesch-Kincaid Grade Level), and vocabulary statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, editors, and other external users use this skill to analyze local text or stdin for counts, readability, vocabulary diversity, and reading or speaking time estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided text files or stdin, so sensitive content may be exposed to the agent's local analysis context.

Mitigation: Use it only on text or file paths intentionally provided, and avoid sensitive files unless local analysis of those contents is intended.

Risk: Readability scores and syllable counts are heuristic and English-optimized, so results can be inaccurate for non-English text or unusual writing.

Mitigation: Treat readability and syllable metrics as estimates, and review important conclusions before relying on them.

## Reference(s):

- [Text Stats on ClawHub](https://clawhub.ai/johnnywang2001/skills/jrv-text-stats)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Plain text metrics or JSON, with shell command examples for use by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports multiple files, stdin input, and compact summary output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
