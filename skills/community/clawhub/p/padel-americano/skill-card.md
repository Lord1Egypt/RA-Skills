## Description:

Create and manage fair-shuffled Padel Americano sessions: register players, generate fixed or open-ended rounds, record game scores, add, remove, or substitute players mid-session, compute official and alternative leaderboards, and export statistics and schedules to PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reditya](https://clawhub.ai/user/reditya)

### License/Terms of Use:

MIT-0

## Use Case:

External organizers and agents use this skill to run Padel Americano events, generate fair rotations, track scores, update rosters during play, view leaderboards, and export event reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF export runs Chrome or Chromium with sandboxing disabled on data loaded from editable tournament JSON files.

Mitigation: Avoid using PDF export on tournament JSON from untrusted people or locations; prefer regenerating state through the CLI, use a dedicated working directory, and isolate PDF export until rendered state fields are fully validated or escaped.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/reditya/skills/padel-americano)
- [Publisher Profile](https://clawhub.ai/user/reditya)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local JSON or PDF artifacts when commands are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI stores tournament state as JSON and can print schedules, scores, and leaderboards or export reports to PDF.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
