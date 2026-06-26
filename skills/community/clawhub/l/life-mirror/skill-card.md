## Description: <br>
Life-Mirror is a Chinese-language life-awareness and relationship-coaching assistant that uses user-authorized personal context, local memory, scheduled check-ins, reports, and role-based guidance to support reflection, planning, and relationship decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lldfjq](https://clawhub.ai/user/lldfjq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Claw or QClaw users use this skill as a persistent personal reflection assistant for emotional support, relationship analysis, life planning, task reminders, and periodic summaries. It is intended for users who explicitly want personal-account syncing, local memory, scheduled reports, and proactive check-ins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad personal-account syncing and persistent profiling. <br>
Mitigation: Connect only the platforms needed for the intended use, avoid payment or work accounts unless necessary, and review or delete stored profile and memory files regularly. <br>
Risk: The skill can create scheduled background sync, report, profile-update, and proactive messaging tasks. <br>
Mitigation: Inspect scheduled jobs before use, disable jobs that are not needed, and keep quiet-hour and daily-message limits aligned with the user's preference. <br>
Risk: The skill stores sensitive personal context locally and uses it to shape future responses. <br>
Mitigation: Choose a private storage directory, restrict local access to that directory, and avoid adding sensitive identifiers unless the user intentionally accepts that storage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lldfjq/life-mirror) <br>
- [README.md](artifact/README.md) <br>
- [Profile sync workflow](artifact/workflows/profile-sync.md) <br>
- [Scheduling workflow](artifact/workflows/scheduling.md) <br>
- [Configuration](artifact/core/config.yaml) <br>
- [Memory model](artifact/core/memory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or text replies, reports, reminders, and optional JSON-style task configuration or local JSON/JSONL memory records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a required response prefix, local profile and memory files, recurring sync/report schedules, and proactive messages.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
