## Description:

Views and searches evolution cycle history with filtering capabilities for tracking progress and analyzing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect local evolution cycle logs, search by result, intent, or keyword, summarize recent activity, and generate history exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that status-file reads can follow symlinks and expose unrelated readable JSON files from the machine.

Mitigation: Use only trusted workspace logs directories; reject symlinks, require regular status_XXXX.json files, and verify resolved paths stay inside the workspace logs directory before broad use.

Risk: Generated Markdown reports or JSON exports can include local cycle history details.

Mitigation: Review generated reports and JSON exports before sharing them outside the intended workspace or team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-cycle-history-viewer)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JavaScript return values, Markdown reports, and JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local logs/status_XXXX.json files and returns filtered cycle records, summaries, reports, or exports.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
