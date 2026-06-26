## Description: <br>
Monitor log files in real-time, filter noise, surface errors, summarize patterns, and alert on anomalies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations engineers use this skill to monitor selected local log files, reduce noisy entries, identify errors and warnings, and summarize recent log patterns for triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured log files may contain secrets, personal data, or other sensitive operational details. <br>
Mitigation: Point the skill only at specific log files you intend to process, avoid broad or sensitive paths, and review log-retention practices before use. <br>
Risk: Heuristic severity detection and summaries may miss context or group unrelated errors together. <br>
Mitigation: Use generated summaries for triage and verify important findings against the original logs or existing monitoring system. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/log-tail-sr) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript code examples and local log summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include filtered log entries, severity labels, counts, error rates, top error groups, and short pattern summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
