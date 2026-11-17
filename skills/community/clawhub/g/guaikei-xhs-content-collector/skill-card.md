## Description:

Collects public Xiaohongshu (XHS/Rednote) content for keyword search, note details, comments, and creator post monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, analysts, and developers use this command skill to retrieve public Xiaohongshu notes, comments, and creator posts for content research, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu query inputs and signed URLs are sent to guaikei.com.

Mitigation: Use the skill only for approved public-data tasks and confirm that third-party API processing is acceptable for the intended workflow.

Risk: GUAIKEI_API_TOKEN is sensitive and may be exposed through shared logs or request traces.

Mitigation: Store the token in environment-secret handling, avoid sharing traces that may include it, and rotate the token if exposure is possible.

Risk: Returned collection results may persist locally in generated logs.

Mitigation: Restrict access to the logs directory and delete generated logs when results should not persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-content-collector)
- [Guaikei service website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration instructions, Files]

**Output Format:** [Markdown instructions with bash commands, structured JSON command results, and optional saved log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and a GUAIKEI_API_TOKEN environment variable; results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
