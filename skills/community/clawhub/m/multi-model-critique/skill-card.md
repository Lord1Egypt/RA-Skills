## Description: <br>
Multi Model Critique routes complex prompts through selected model agents for drafting, cross-critique, revision, and final synthesis with uncertainties and evidence notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prairiedoggg](https://clawhub.ai/user/prairiedoggg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when a task is explicitly complex and benefits from multiple model drafts, peer critique, revision, scoring, and a synthesized final answer. It is suited to high-stakes, ambiguous, or long-form reasoning where the user wants uncertainties and evidence notes surfaced. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complex prompts may contain sensitive information routed to selected model agents. <br>
Mitigation: Avoid sending highly sensitive information unless the selected agents are trusted and approved for that data. <br>
Risk: Multi-agent critique runs can consume more time or budget than a single-model response. <br>
Mitigation: Set runtime controls such as budgetUsd, timeoutSec, maxRetries, and maxRounds before running costly tasks. <br>
Risk: Generated prompt files or run-plan artifacts may retain user content after execution. <br>
Mitigation: Delete generated prompt and run-plan files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/prairiedoggg/multi-model-critique) <br>
- [Orchestration Template](references/orchestration-template.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown final answer or JSON matching references/output-schema.md; helper scripts may generate prompt files and run-plan JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes per-model scoring, uncertainties, optional next steps, and runtime controls for timeouts, retries, rounds, and budget.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
