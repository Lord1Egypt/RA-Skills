## Description: <br>
Analyze model training or inference resource behavior from profiler artifacts, with focus on GPU memory (VRAM) and CPU hotspots. Uses JSON/JSON.GZ artifacts only to avoid unsafe deserialization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daiwk](https://clawhub.ai/user/daiwk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ML engineers use this skill to analyze trusted PyTorch CUDA memory snapshots and profiler traces, identify GPU memory pressure and CPU bottlenecks, and prepare a ranked optimization plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profiler artifacts may contain private model, workload, path, or host details. <br>
Mitigation: Analyze only trusted local files that the user intentionally provides, and avoid pointing the analyzer at unrelated private files. <br>
Risk: Unsafe serialized profiler inputs can execute code or hide behavior if deserialized. <br>
Mitigation: Use only JSON or JSON.GZ artifacts; the analyzer rejects pickle input and asks users to re-export snapshots as JSON in their own trusted environment. <br>
Risk: Optimization recommendations can be misleading when traces are incomplete or the target phase is unclear. <br>
Mitigation: Label low-confidence conclusions as hypotheses, capture run context, and validate each action with a measurable follow-up profiler metric. <br>


## Reference(s): <br>
- [Model Resource Profiler on ClawHub](https://clawhub.ai/daiwk/model-resource-profiler) <br>
- [Interpretation Guide](references/interpretation.md) <br>
- [Analyzer Implementation](scripts/analyze_profile.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON reports with concise diagnostic guidance and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected local JSON or JSON.GZ profiler artifacts and rejects pickle input.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
