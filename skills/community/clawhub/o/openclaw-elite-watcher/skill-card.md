## Description:

Provides OpenClaw ecosystem intelligence summaries intended to monitor protocol and contributor activity and distill changes into strategy reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw ecosystem watchers use this skill to request concise intelligence reports about OpenClaw repository and contributor activity. Server security evidence says the current artifact should be treated as review material until real data collection, evidence-backed reporting, and safer report-writing behavior are added.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may be misleading because server security evidence says the current artifact claims real-time intelligence while producing hard-coded content.

Mitigation: Treat generated reports as unverified until the skill implements real data collection and evidence-backed reporting; review cited source activity before using summaries.

Risk: A generated daily report may overwrite an existing report and writes to a user-specific path.

Mitigation: Use a user-selected output path and non-overwriting filenames or explicit overwrite confirmation before deployment.

Risk: Installation risk is higher when filesystem writes and data-access expectations are not clear.

Mitigation: Document the report output location and any network or data-access permissions before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmstudio667-commits/skills/openclaw-elite-watcher)
- [OpenClaw repository](https://github.com/openclaw/openclaw)
- [Peter Steinberger GitHub profile](https://github.com/steipete)
- [OpenClaw X profile](https://x.com/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a daily intelligence report file; server security evidence says the current report content is hard-coded and may overwrite an existing daily report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
