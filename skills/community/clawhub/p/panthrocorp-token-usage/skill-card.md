## Description: <br>
Multi-agent token burn analysis across all registered OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panthrocorp](https://clawhub.ai/user/panthrocorp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to analyze token usage, estimated costs, and anomalies across registered OpenClaw agents. It summarizes per-agent and combined usage, then persists structured history for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage history can retain metadata about agent runs, models, timestamps, token usage, and estimated costs. <br>
Mitigation: Review the storage location before installing, use it only in workspaces where this metadata retention is acceptable, and delete or rotate old records according to local policy. <br>
Risk: The skill always appends structured history for each run. <br>
Mitigation: Confirm the history file path and retention expectations before use; avoid sensitive workspaces unless the retained metadata is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panthrocorp/panthrocorp-token-usage) <br>
- [OpenClaw skills homepage](https://github.com/PanthroCorp-Limited/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files] <br>
**Output Format:** [Markdown report plus compact JSON Lines history record] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends a token-usage-history.ndjson record on each run; optional token-diet-log.md logging occurs only when explicitly requested.] <br>

## Skill Version(s): <br>
0.2.2 (source: frontmatter, changelog, version.txt, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
