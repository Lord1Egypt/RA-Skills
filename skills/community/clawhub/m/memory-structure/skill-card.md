## Description: <br>
Enable AI to learn from mistakes and never repeat them through error tracking, layered memory, regular self-reflection, and continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangssi1998-cell](https://clawhub.ai/user/wangssi1998-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a local memory structure for tracking preferences, patterns, rules, corrections, and self-reflection state across agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can accumulate secrets or sensitive personal data if users place that information in memory files. <br>
Mitigation: Use a dedicated directory, review entries periodically, and avoid storing secrets or sensitive personal data. <br>
Risk: Recurring heartbeat checks can automatically update local memory state. <br>
Mitigation: Enable recurring heartbeat checks only when automatic local memory updates are acceptable for the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangssi1998-cell/memory-structure) <br>
- [Setup guide](artifact/setup.md) <br>
- [Heartbeat rules](artifact/heartbeat-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory templates and setup guidance; no code execution, credentials, or external data sharing are included.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
