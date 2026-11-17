## Description:

InkPot is a Chinese-language knowledge management skill that records learning topics, user activity, profile signals, review candidates, search results, statistics, and exported knowledge-base content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use InkPot to maintain a local Chinese-language learning knowledge base, record study behavior, search saved topics, review weak areas, and generate recommendations from stored notes and profile signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill attempts always-on monitoring and persistent profiling across conversations.

Mitigation: Install it only when continuous local knowledge capture is desired, prefer explicit commands, and avoid adding auto-load instructions to persistent memory unless the user has knowingly consented.

Risk: The skill stores notes, learning logs, and profile information in local files.

Mitigation: Review stored files regularly and avoid recording sensitive personal, credential, or confidential business information.

Risk: The Python CLI can write files based on category and topic inputs before path validation is fixed.

Mitigation: Use trusted category and topic names only, and inspect generated file paths before relying on or sharing the resulting knowledge base.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/inkpot)
- [Publisher profile](https://clawhub.ai/user/fslong520)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown and plain text responses with optional Python CLI commands and local knowledge-base file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local note records, profile updates, search results, review recommendations, statistics, and exported knowledge-base content.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
