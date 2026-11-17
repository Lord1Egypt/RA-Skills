## Description:

Helps agents plan and evaluate context compression strategies for long-running sessions, large codebases, token reduction, structured summarization, and tokens-per-task optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lidekahdjdhdhsjjs-lang](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to decide when to compress context, preserve file and decision history, and evaluate whether compressed summaries still support task continuation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context compression can omit file paths, error messages, decisions, or next steps that an agent needs to continue work.

Mitigation: Use structured summaries with explicit sections for session intent, modified files, read files, decisions, current state, and next steps.

Risk: Opaque or aggressive compression can make it hard to verify what information was preserved.

Mitigation: Prefer anchored iterative summaries when interpretability and artifact tracking matter, and evaluate summaries with recall, artifact, continuation, and decision probes.

Risk: Evaluating real conversation history may expose file names, errors, and decisions to any external model or process connected later.

Mitigation: Keep evaluation local unless an external judge is intentionally configured, and avoid sending sensitive conversation history to unapproved services.

## Reference(s):

- [Context Compression Evaluation Framework](references/evaluation-framework.md)
- [ClawHub Skill Page](https://clawhub.ai/lidekahdjdhdhsjjs-lang/skills/hz-context-optimizer)
- [Publisher Profile](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang)
- [Artifact Repository](https://github.com/lidekahdjdhdhsjjs-lang/Huizai-openclaw)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown guidance with optional Python helper code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured summaries, evaluation probes, scoring guidance, and local helper code for compression assessment.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
