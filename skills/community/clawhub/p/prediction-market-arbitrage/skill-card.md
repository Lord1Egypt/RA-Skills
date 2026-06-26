## Description: <br>
Orchestrates topic monitoring, Polymarket odds lookups, and execution-pattern guidance to detect news-market probability gaps and produce alert-first arbitrage recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to coordinate installed ClawHub skills for monitoring CEO/company event signals, comparing them with Polymarket probabilities, and producing alert-only or execution-plan recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can influence financial decisions and optional trade planning. <br>
Mitigation: Use alert-only or dry-run mode by default, review recommendations manually, and require explicit user confirmation before any live trade. <br>
Risk: Trade-capable execution depends on an external API key and installed dependency skills. <br>
Mitigation: Provide SIMMER_API_KEY only when trade-capable workflows are intended, and review the topic-monitor, polymarket-odds, and simmer-weather skills before use. <br>
Risk: Refreshing all local skills may change dependency behavior. <br>
Mitigation: Avoid update --all unless the user intentionally wants dependency updates, and re-check installed skill versions after updating. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h4gen/prediction-market-arbitrage) <br>
- [Inspected upstream skills](references/inspected-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command blocks and structured signal fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include alert-only recommendations, dry-run execution plans, confidence deltas, and no-trade outcomes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
