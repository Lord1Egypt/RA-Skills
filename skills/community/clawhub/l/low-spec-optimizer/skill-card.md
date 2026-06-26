## Description: <br>
Helps agents optimize OpenClaw on low-resource machines by checking system load, cleaning stale sessions and caches, and recommending lightweight configuration settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lunaviva211-sketch](https://clawhub.ai/user/lunaviva211-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to monitor constrained machines, decide when to reduce workload, clean stale local state, and apply lower-resource configuration recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup actions can remove local sessions, caches, and broader system state than a user may expect. <br>
Mitigation: Run cleanup with --dry-run first, review the listed targets, and use --aggressive only when intentionally clearing npm, pip, and journal data. <br>
Risk: The cleanup script uses hard-coded /home/nvi paths and includes stale-session cleanup logic that may not match every installation. <br>
Mitigation: Adjust paths for the target environment and test cleanup on non-critical session history before relying on it for important OpenClaw data. <br>


## Reference(s): <br>
- [Low-Spec Configuration Guide](references/config-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Resource checker script emits JSON system metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
