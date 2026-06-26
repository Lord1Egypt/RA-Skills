## Description: <br>
Provides Node.js V8 heap snapshot diagnostics and perf_hooks-based performance profiling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amd5](https://clawhub.ai/user/amd5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for on-demand local Node.js memory diagnostics, heap snapshot generation, and timing profile reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heap snapshot files can contain secrets, tokens, user content, or other application data captured from process memory. <br>
Mitigation: Keep generated heap snapshots private, restrict access to diagnostic artifacts, and delete them after analysis. <br>
Risk: The skill writes local diagnostic files under the user's home directory, which may persist beyond the debugging session. <br>
Mitigation: Review and clean up generated heap snapshot, diagnostics, profiler state, and history files when they are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated local diagnostic files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates heap snapshots, diagnostics JSON, profiler state, history, and text reports under the user's local home directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
