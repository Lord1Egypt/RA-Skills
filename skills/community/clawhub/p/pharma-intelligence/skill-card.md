## Description:

In-depth, multi-region pharmaceutical intelligence search and synthesis for drug approvals, clinical trials, regulatory submissions, pipeline assets, patent landscapes, competitive intelligence, scientific evidence, disease targets, genetic associations, and compound bioactivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and analysts use this skill to gather source-grounded pharmaceutical and biomedical intelligence across regulatory, clinical, literature, patent, safety, target-discovery, and bioactivity sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can make broad public API and web requests, and untrusted URL or path inputs could steer the agent outside the intended biomedical sources.

Mitigation: Run the skill in a sandboxed agent runtime, keep filesystem write access limited, and restrict requests to the documented public biomedical sources.

Risk: Prompts or retrieved content could influence tool parameters such as base_url, path, query_path, or raw_output_path.

Mitigation: Require user oversight for tool inputs and review generated commands or saved-output paths before execution in sensitive environments.

Risk: Pharmaceutical evidence can be incomplete, stale, region-specific, or blocked by source availability.

Mitigation: Prefer official regulatory and trial registry sources, cite source tier and access date, rerun live searches for current answers, and clearly label unresolved gaps or conflicts.

## Reference(s):

- [Sub-Skills Quick Reference](references/sub-skills.md)
- [Sources by Region](references/sources-by-region.md)
- [Pharma Intelligence Workflow](references/pharma-intelligence-workflow.md)
- [Drug Naming Conventions by Region](references/drug-naming.md)
- [Regulatory Timelines by Agency](references/regulatory-timelines.md)
- [ClawHub Skill Page](https://clawhub.ai/sciminer/skills/pharma-intelligence)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, tables, cited findings, JSON API request examples, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite source tier and access date, distinguish missing data from negative findings, and save raw API payloads only when requested.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
