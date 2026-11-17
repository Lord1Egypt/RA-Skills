## Description:

Log heart rate readings, track BPM trends, and set cardiovascular goals. Use when recording heart rate, tracking trends, or charting weekly averages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal health trackers use this skill to record local heart-rate entries, inspect recent activity, view basic statistics, and export local logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heart-rate entries and related notes are stored as local plaintext files under ~/.local/share/heartrate.

Mitigation: Use only on trusted machines, review directory permissions, and avoid entering sensitive notes on shared systems.

Risk: The advertised trend, analytics, and export behavior is under-scoped and may not work as described.

Mitigation: Review the skill before installing and validate exported or summarized results before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/heartrate)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text CLI output and local export files in JSON, CSV, or TXT]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local plaintext logs under ~/.local/share/heartrate.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
