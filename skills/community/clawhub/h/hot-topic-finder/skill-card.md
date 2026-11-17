## Description:

Finds and tracks topic ideas, checks prior use, and recommends fresh topics using local topic history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linus995](https://clawhub.ai/user/linus995)

### License/Terms of Use:


## Use Case:

Creators, content planners, and agents use this skill to generate topic ideas, avoid repeating recently used topics, and review local topic usage history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release describes live multi-platform hot-topic monitoring, but the security evidence says the code uses a small built-in topic list and local history database.

Mitigation: Treat recommendations as local helper output, verify trends against current external sources, and do not rely on the skill for real-time news or crisis monitoring.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and writes topic history to a local SQLite database under ~/.openclaw/data/topic_history.db.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
