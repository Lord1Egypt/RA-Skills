## Description:

Analyze BrainNode protobuf recordings from this autonomous-driving project against a natural-language problem description, identify the most likely faulty module, and produce an evidence-based module analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[narol1024](https://clawhub.ai/user/narol1024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers investigating BrainNode autonomous-driving recordings use this skill to match a reported symptom to upstream module evidence and produce a bounded module diagnosis. It is intended for protobuf runtime logs and related replay or dump analysis across sensor, perception, localization, planning, control, chassis, task, and diagnostics data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can execute Python code from a target project's protobuf directory when loading generated BrainNode bindings.

Mitigation: Use only trusted BrainNode repositories and trusted generated protobuf bindings; avoid untrusted --repo-root or --proto-dir values and prefer a sandboxed, runtime-limited environment.

Risk: Large protobuf recordings may be read into memory during triage.

Mitigation: Use --max-files and --max-file-bytes to narrow scanning, and split long recordings before deep inspection.

Risk: The skill reads project PB files and can optionally write a JSON report.

Mitigation: Run it only on approved recordings and choose an explicit output path for generated reports.

## Reference(s):

- [BrainNode PB Module Signals](references/module-signals.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown analysis report in Chinese by default, with optional JSON report output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes a suspected module, confidence rating, evidence summary, module-by-module reasoning, and minimum next checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
