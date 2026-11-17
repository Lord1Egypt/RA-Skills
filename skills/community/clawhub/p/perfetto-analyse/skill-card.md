## Description:

Captures and analyzes Android Perfetto traces via CLI and config files, covering trace collection for CPU, GPU, memory, rendering, and power, TraceConfig editing, and analysis of jank, latency, overdraw, and power in Perfetto UI or trace_processor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkecoding](https://clawhub.ai/user/linkecoding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and performance engineers use this skill to capture Android Perfetto traces, select or edit TraceConfig files, and analyze jank, latency, overdraw, CPU scheduling, GPU rendering, memory, and power behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Android trace data can contain sensitive application, device, timing, and process information.

Mitigation: Install and run the skill only in environments where Android trace data can be handled safely.

Risk: The helper depends on the Perfetto Python package and may direct users to download a trace_processor binary.

Mitigation: Prefer pinned and reviewed dependency versions, verify downloaded trace_processor binaries when possible, and avoid running install or analysis commands as root or with unnecessary privileges.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkecoding/skills/perfetto-analyse)
- [Perfetto Configuration Reference](artifact/reference.md)
- [Perfetto UI](https://ui.perfetto.dev)
- [TraceConfig Reference](https://perfetto.dev/docs/reference/trace-config-proto)
- [Trace Processor](https://perfetto.dev/docs/analysis/trace-processor)
- [Trace Processor Python](https://perfetto.dev/docs/analysis/trace-processor-python)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands, PerfettoSQL examples, and TraceConfig snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local .pbtx.txt templates and a Python trace query helper for command-line analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
