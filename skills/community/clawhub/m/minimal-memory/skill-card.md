## Description:

Maintain clean, efficient memory files with GOOD/BAD/NEUTRAL categorization and semantic search for agent memory management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zencrust-ai](https://clawhub.ai/user/zencrust-ai)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to maintain persistent local memory, categorize entries as GOOD, BAD, or NEUTRAL, search prior memory files, and review or archive stale daily notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores persistent local memory files that may contain sensitive or private details if users add them.

Mitigation: Avoid storing secrets, credentials, private personal details, or untrusted copied text without review.

Risk: Daily memory entries can be promoted into long-term MEMORY.md and influence future agent behavior.

Mitigation: Review and condense entries before promoting them into long-term memory.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and local memory file conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and searches local Markdown memory files under configurable workspace paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
