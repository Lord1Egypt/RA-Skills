## Description: <br>
Captures and analyzes Android Perfetto traces via CLI and config files, covering trace collection, TraceConfig editing, and analysis of jank, latency, overdraw, and power. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkecoding](https://clawhub.ai/user/linkecoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to collect Android Perfetto traces, tune TraceConfig files, and analyze traces for CPU scheduling, rendering jank, latency, overdraw, and power behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Perfetto trace capture can collect sensitive device, app, timing, or process information. <br>
Mitigation: Limit collection to the intended device, app, and time window, and treat generated trace files as sensitive. <br>
Risk: adb and Perfetto commands can run device-side collection or leave background capture active. <br>
Mitigation: Review commands and TraceConfig files before execution, and stop any background capture promptly. <br>
Risk: Installing trace processing tooling from untrusted locations could introduce supply-chain risk. <br>
Mitigation: Install Perfetto tooling only from trusted sources. <br>


## Reference(s): <br>
- [Perfetto configuration reference](reference.md) <br>
- [CPU-only TraceConfig template](configs/cpu_only.pbtx.txt) <br>
- [UI jank TraceConfig template](configs/ui_jank.pbtx.txt) <br>
- [Power TraceConfig template](configs/power.pbtx.txt) <br>
- [Trace query helper script](scripts/query_trace.py) <br>
- [Perfetto UI](https://ui.perfetto.dev) <br>
- [TraceConfig Reference](https://perfetto.dev/docs/reference/trace-config-proto) <br>
- [Trace Processor](https://perfetto.dev/docs/analysis/trace-processor) <br>
- [Trace Processor Python](https://perfetto.dev/docs/analysis/trace-processor-python) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, TraceConfig snippets, and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce PerfettoSQL queries, adb/perfetto commands, and configuration templates for trace capture and analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
