## Description: <br>
Vesper generates morning, evening, and on-demand briefings by aggregating calendar, message, portfolio, proposal, and journal signals into concise natural-language summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users of the OpenClaw Agent Suite use Vesper to receive scheduled or on-demand daily briefings that summarize actionable events, messages, logistics, markets, and pending decisions without exposing internal analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill aggregates sensitive personal data from calendar, messages, finance, travel, journals, and other skills. <br>
Mitigation: Install only in workspaces where this cross-skill access is acceptable, and limit use with sensitive data unless the user has reviewed the data paths. <br>
Risk: Initialization can register recurring morning, evening, and midnight self-update jobs. <br>
Mitigation: Review scheduled jobs after installation and disable or adjust any job that is not appropriate for the environment. <br>
Risk: The self-update command can replace local skill files from a remote source. <br>
Mitigation: Prefer manual updates from a pinned trusted version or disable the midnight update job when change control is required. <br>
Risk: Broad invocation phrases could trigger briefings or status checks in contexts involving sensitive calendar, message, financial, or travel data. <br>
Mitigation: Narrow invocation phrases and require explicit user intent before generating or delivering briefings in sensitive contexts. <br>


## Reference(s): <br>
- [Vesper Skill Page](https://clawhub.ai/indigokarasu/ocas-vesper) <br>
- [Vesper Schemas](references/schemas.md) <br>
- [Vesper Briefing Templates](references/briefing_templates.md) <br>
- [Vesper Signal Filtering](references/signal_filtering.md) <br>
- [Vesper Journal](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML, JSON, configuration, shell commands, guidance] <br>
**Output Format:** [Plain text or minimal HTML briefings with JSON briefing and journal records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local briefing, signal evaluation, decision, and journal records; scheduled briefing and update jobs may be registered during initialization.] <br>

## Skill Version(s): <br>
2.7.0 (source: release evidence, skill.json, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
