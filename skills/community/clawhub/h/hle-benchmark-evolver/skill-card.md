## Description:

Runs HLE-oriented benchmark reward ingestion and curriculum generation for capability-evolver.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to ingest Humanity's Last Exam benchmark reports, convert results into reward state, generate curriculum focus signals, and run benchmark-linked evolution loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pipeline can run arbitrary local shell commands through evaluator command arguments.

Mitigation: Install only for trusted users or automation, avoid untrusted evaluator templates, and prefer sandboxed or allowlisted evaluator wrappers.

Risk: Pipeline execution can trigger broader evolution and solidify actions.

Mitigation: Keep solidify dry-run enabled unless mutation is intended, and review pipeline arguments before execution.

Risk: Untrusted benchmark report paths or malformed report inputs may affect local workflow state.

Mitigation: Use trusted report paths, validate report provenance, and run the skill in a scoped workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/hle-benchmark-evolver)
- [Publisher profile](https://clawhub.ai/user/wanng-ide)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result output includes benchmark identifiers, accuracy, reward, trend, curriculum stage, queue size, focus areas, and next questions.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
