## Description: <br>
QMD memory system telemetry for measuring index health, BM25 retrieval quality, coverage maps, and trend analysis in a local QMD memory backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers operating QMD and OpenClaw memory systems use this skill to run local diagnostics for retrieval quality, index freshness, gateway activity, and collection coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory diagnostics may reveal sensitive topics, source locations, and detailed retrieval snapshots. <br>
Mitigation: Review or edit the hard-coded query list before running, use --dry-run first, and confirm that local snapshots and local Langfuse logging are acceptable in the target environment. <br>
Risk: The probe is specific to a QMD and OpenClaw setup and can produce incomplete or misleading results outside that environment. <br>
Mitigation: Install only where the expected qmd binary, OpenClaw gateway logs, and local telemetry services are present, then review results before acting on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nissan/memory-health-probe) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and local diagnostic output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local QMD memory telemetry, JSON snapshots, trend summaries, and optional local Langfuse traces.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
