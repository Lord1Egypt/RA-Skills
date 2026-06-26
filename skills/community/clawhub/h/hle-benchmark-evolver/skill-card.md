## Description: <br>
Runs HLE-oriented benchmark reward ingestion and curriculum generation for capability-evolver. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to ingest Humanity's Last Exam benchmark reports, convert question-level results into reward signals, and generate an easy-first curriculum queue for capability-evolver workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The benchmark pipeline can execute a user-provided evaluator command through --eval_cmd. <br>
Mitigation: Only pass evaluator commands from trusted sources, avoid untrusted paths or input, and run the pipeline in a sandboxed environment without sensitive credentials. <br>
Risk: Pipeline mode can mutate local evolver state when evolution and solidification are enabled. <br>
Mitigation: Run result mode first, review the generated summary, and use --skip_evolve=true unless state changes are intended. <br>
Risk: The skill depends on local capability-evolver or feishu-evolver-wrapper code being present and trustworthy. <br>
Mitigation: Install only in workspaces where those local dependencies have been reviewed and scanned before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/hle-benchmark-evolver) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Sample HLE report](artifact/assets/hle_report.sample.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON result summaries and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs compact benchmark progress metrics, curriculum stage, queue size, focus subjects, focus modalities, and next questions.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
