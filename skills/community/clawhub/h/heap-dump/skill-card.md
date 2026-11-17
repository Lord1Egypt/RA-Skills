## Description:

Generates V8 heap snapshots and perf_hooks profiling output for local Node.js and OpenClaw diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amd5](https://clawhub.ai/user/amd5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to capture local heap snapshots, inspect memory diagnostics, and track perf_hooks checkpoints during performance investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heap snapshots and diagnostic files can be large and may contain runtime details.

Mitigation: Run the skill only when local diagnostics are needed, restrict access to generated files, and delete snapshots after analysis.

Risk: Profiler state and history persist locally under ~/.openclaw/profiles/.

Mitigation: Review and remove profiler history when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amd5/skills/heap-dump)

## Skill Output:

**Output Type(s):** [text, files, shell commands]

**Output Format:** [Console text plus local .heapsnapshot, JSON diagnostics, and JSONL/profile state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local diagnostic files under ~/.openclaw; generated snapshots and profiler history may need manual cleanup.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
