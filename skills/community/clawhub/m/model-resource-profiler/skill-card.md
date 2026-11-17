## Description:

Analyze model training or inference resource behavior from profiler artifacts, with focus on GPU memory (VRAM) and CPU hotspots. Uses JSON/JSON.GZ artifacts only to avoid unsafe deserialization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daiwk](https://clawhub.ai/user/daiwk)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to analyze trusted local PyTorch profiler and CUDA memory snapshot JSON artifacts, identify CPU and GPU memory bottlenecks, and produce prioritized optimization actions with validation metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profiler artifacts can come from untrusted or unknown training environments.

Mitigation: Use the skill only with trusted local JSON/JSON.GZ artifacts and confirm the trust boundary before analysis.

Risk: Legacy pickle memory snapshots can execute unsafe deserialization paths in other workflows.

Mitigation: Do not analyze pickle snapshots; re-export the data as JSON in the user's trusted training environment.

Risk: Reports may be written outside the intended workspace if broad output paths are supplied.

Mitigation: Provide explicit output paths, preferably in a temporary or project-local directory.

## Reference(s):

- [Interpretation Guide](references/interpretation.md)
- [Analyzer Implementation](scripts/analyze_profile.py)
- [ClawHub Skill Page](https://clawhub.ai/daiwk/skills/model-resource-profiler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON analysis files, shell commands, and optimization guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local JSON/JSON.GZ profiler artifacts and can write markdown and JSON report files.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
