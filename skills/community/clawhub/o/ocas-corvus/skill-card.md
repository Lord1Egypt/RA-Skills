## Description: <br>
Corvus analyzes behavioral patterns, detects routines, finds anomalies in the knowledge graph, and runs exploration cycles across accumulated activity signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Corvus to analyze accumulated knowledge-graph and journal signals for routines, emerging interests, stalled threads, anomalies, and cross-domain opportunities. The skill produces validated proposals and behavioral signals for downstream skills after multi-signal corroboration and falsification checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent cron and heartbeat jobs can run broad journal and knowledge-graph analysis without fresh user review. <br>
Mitigation: Disable the scheduled jobs by default or require explicit approval before registering cron and heartbeat entries. <br>
Risk: Silent self-updates from a mutable branch can change skill behavior after installation. <br>
Mitigation: Disable unattended updates, pin reviewed versions, or require user approval before applying downloaded updates. <br>
Risk: Validated proposals can write into downstream skill intake directories and influence later agent behavior. <br>
Mitigation: Confirm the intended downstream intake directories and review generated BehavioralSignal and InsightProposal files before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/indigokarasu/ocas-corvus) <br>
- [Curiosity Engine](references/curiosity_engine.md) <br>
- [Pattern Engines](references/pattern_engines.md) <br>
- [Schemas](references/schemas.md) <br>
- [Journal](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured JSON/JSONL files with optional shell commands for initialization and updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes hypotheses, patterns, proposals, decisions, journals, BehavioralSignal files, and InsightProposal files under the configured OpenClaw data directories.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata, artifact skill.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
