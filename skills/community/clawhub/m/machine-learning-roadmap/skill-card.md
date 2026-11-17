## Description:

Provides shell commands for recording, reviewing, searching, and exporting machine-learning-related content notes in local log files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to capture drafts, outlines, headlines, translations, and related ML-content planning notes, then inspect recent entries or export the retained data. Users should treat it as a local content logger rather than a complete machine-learning study roadmap planner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is labeled as an ML roadmap planner but primarily stores and exports local content notes.

Mitigation: Install it only when a local ML-content note logger is intended, and review the available commands before use.

Risk: Drafts, translations, and other entries are retained under ~/.local/share/machine-learning-roadmap and may include sensitive user-provided text.

Mitigation: Avoid entering secrets or sensitive drafts, and manually review or delete the data directory when retained entries are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/machine-learning-roadmap)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Plain text command output with optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped entries and export files under ~/.local/share/machine-learning-roadmap.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
