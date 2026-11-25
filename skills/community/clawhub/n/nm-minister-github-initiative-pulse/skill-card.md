## Description:

Generates markdown digests and CSV exports for GitHub initiative health

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use the skill to summarize initiative progress, blockers, risks, and milestones from tracker and GitHub Projects data. They can prepare Markdown updates for GitHub discussions and export initiative health data as CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad “status” trigger could conflict with another skill or workflow in the agent setup.

Mitigation: Check trigger mappings in the intended setup and confirm that requests for status reporting invoke the desired skill.

Risk: Digests and CSV exports may expose repository, issue, pull request, or tracker details when shared.

Mitigation: Check the destination repository’s audience and the contents of links and tracker fields before posting or distributing exports.

Risk: Security analysis is partial because a referenced local path was missing.

Mitigation: Review the referenced local path and the affected skill behavior before installation; rerun the security analysis when complete coverage is available.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/minister)

## Skill Output:

**Output Type(s):** [Markdown, CSV]

**Output Format:** [Markdown digests and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initiative summaries based on tracker data and GitHub board metadata.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
