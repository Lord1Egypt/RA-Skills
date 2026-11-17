## Description:

Move Planner helps an agent manage residential move logistics, including timelines, tasks, vendors, address changes, budgets, and buy or sell milestones in a local tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

External users planning, executing, or closing out a residential move use this skill to keep move dates, tasks, vendors, budget items, address changes, and closing milestones organized in one local tracker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local tracker can contain personal move details such as addresses, household notes, vendor information, and budget items.

Mitigation: Keep move-data.json in a user-controlled local workspace and avoid entering full account numbers, SSNs, passport numbers, driver's license numbers, or mortgage application documents.

Risk: The evidence notes a documentation mismatch about whether move-data.json is stored in the working directory or the skill data directory.

Mitigation: Clarify the intended storage path before deployment and verify the agent only reads and writes the expected local tracker file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris/skills/move-planner)
- [Publisher profile](https://clawhub.ai/user/chris)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, guidance]

**Output Format:** [Conversational Markdown summaries with local JSON tracker updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists move state in move-data.json and may produce local printable timelines, vendor lists, or move-day plans.]

## Skill Version(s):

1.0.2 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
