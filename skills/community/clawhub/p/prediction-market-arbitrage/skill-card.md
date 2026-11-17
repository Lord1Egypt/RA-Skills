## Description:

Orchestrates monitoring, market odds, and execution proxy tools to detect news-market price gaps and emit arbitrage alerts with optional trade plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

Developers and market-analysis operators use this skill to coordinate news monitoring, Polymarket probability lookup, and guarded execution planning for prediction-market mispricing alerts. The workflow is alert-first and requires explicit user confirmation before any live trading step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote install commands and `update --all` can change unrelated installed skills or pull newer behavior than the skill was authored against.

Mitigation: Review install steps before use, prefer pinned ClawHub and upstream skill versions, and avoid broad update commands in controlled environments.

Risk: Trading credentials could be exposed or used during setup or execution planning.

Mitigation: Run installation without `SIMMER_API_KEY` in the environment, treat execution-plan output as manual guidance, require a dry run, and obtain explicit confirmation before any live trade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h4gen/skills/prediction-market-arbitrage)
- [ClawHub publisher profile](https://clawhub.ai/user/h4gen)
- [Inspected upstream skills](references/inspected-skills.md)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured fields and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include alert-only recommendations or manual execution plans; live trading requires explicit user opt-in.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
