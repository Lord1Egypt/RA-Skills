## Description: <br>
MacBook system optimization, performance monitoring, and troubleshooting tools for macOS users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drg3nz0](https://clawhub.ai/user/drg3nz0) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External macOS users use this skill to ask an agent for system health checks, performance troubleshooting, disk cleanup recommendations, process review, and GUI-guided optimization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide cleanup or system changes that affect user files, login items, background services, cron jobs, or power settings. <br>
Mitigation: Start with read-only health checks, require a preview before any change, and approve each cleanup or system setting change one at a time. <br>
Risk: Broad macOS permissions such as Full Disk Access or Accessibility can increase the impact of agent mistakes. <br>
Mitigation: Avoid granting broad permissions unless a specific task requires them, and revoke them after the task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drg3nz0/macbook-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/drg3nz0) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and step-by-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include visual summaries, cleanup previews, and macOS GUI navigation steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
