## Description:

A prompt-only Chinese-language assistant that researches income opportunities, evaluates markets and competitors, tracks income progress, and generates actionable money-making reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bandwe](https://clawhub.ai/user/bandwe)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent to research Chinese-market income opportunities, score them, compare competitors, track monthly income goals, and produce Markdown action plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External platform research and generated income guidance may be incomplete, stale, or misleading.

Mitigation: Review opportunities, platform rules, pricing assumptions, and action plans before acting on them.

Risk: Income details, business plans, or progress history may be retained in local files or agent memory.

Mitigation: Avoid sensitive details unless retention is acceptable, and ask the agent to confirm before writing income_database.json or storing memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bandwe/skills/money-maker-hand)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with optional JSON/TOML snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local state files and agent memory when the runtime provides those capabilities.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
