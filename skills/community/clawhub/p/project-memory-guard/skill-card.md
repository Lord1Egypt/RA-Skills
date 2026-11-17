## Description:

Project Memory Guard validates proposed project-memory writes against project boundaries and writeback rules before records are accepted, rejected, or rerouted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check whether content can safely enter project memory, including notes, findings, tasks, summaries, migrated records, and imported messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence whether memory records are accepted, rejected, or rerouted.

Mitigation: Review decisions before automated writeback and keep rerouted or low-confidence records in an inbox or cleanup flow for human confirmation.

Risk: The artifact uses candidate_project_id in the input schema but project_id in the hard-rule table.

Mitigation: Confirm the project identifier field mapping before operational use so valid records are not incorrectly rejected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunbinnju-star/skills/project-memory-guard)
- [Publisher profile](https://clawhub.ai/user/sunbinnju-star)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured decision record with destination, normalized record, contamination risk, missing fields, and reason]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces accept, reject, or reroute decisions and may normalize accepted or rerouted records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
