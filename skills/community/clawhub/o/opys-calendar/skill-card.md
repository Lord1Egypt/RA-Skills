## Description:

A local markdown-backed calendar with CLI and optional two-way Google Calendar sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[21j3phy](https://clawhub.ai/user/21j3phy)

### License/Terms of Use:


## Use Case:

Developers and calendar users use this skill to let agents read, summarize, update, import, export, and sync a local markdown-backed schedule while preserving event identity and overlap handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weakly scoped local APIs can expose or mutate calendar data.

Mitigation: Run the skill only on a trusted local machine and do not expose port 8787 to a network.

Risk: Google Calendar sync can grant broad calendar access and stores OAuth tokens in plaintext.

Mitigation: Enable Google sync only after accepting that access level, and address plaintext token storage before broader reuse.

Risk: The artifact ships real-looking personal calendar metadata, sync state, snapshots, and settings.

Mitigation: Remove packaged runtime calendar files from reusable copies and add them to ignore or release-exclusion rules.

Risk: Security guidance calls out flagged dependencies.

Mitigation: Update flagged dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/21j3phy/skills/opys-calendar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to update local calendar Markdown, JSON settings, snapshots, and optional Google Calendar sync state.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
