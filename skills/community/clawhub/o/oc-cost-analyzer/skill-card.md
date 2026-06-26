## Description: <br>
Analyzes OpenClaw token usage and cost from local session logs, identifies high-cost patterns such as long conversations, frequent cron runs, large context, and expensive models, and produces cost optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local conversation logs, estimate model and token costs, and generate practical recommendations for lowering recurring AI usage costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The analyzer reads local OpenClaw conversation logs, which may contain sensitive conversation content. <br>
Mitigation: Run it only in a trusted local workspace and review the generated report location and file permissions before sharing results. <br>
Risk: Optimization suggestions may include model-switching, cron, fallback, Ollama, or cleanup commands that change local configuration or delete old memory files if copied manually. <br>
Mitigation: Review each suggested command before running it, and avoid destructive cleanup commands unless the target files have been backed up or confirmed unnecessary. <br>
Risk: Cost estimates depend on the model pricing table bundled in the script and can become stale. <br>
Mitigation: Verify current model prices before making budget decisions or editing the script's pricing table. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dagangtj/oc-cost-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Console text and a Markdown cost analysis report with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is written locally to the OpenClaw workspace memory directory when the analyzer command is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
