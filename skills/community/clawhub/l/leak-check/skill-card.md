## Description: <br>
Scan session logs for leaked credentials. Checks JSONL session files against known credential patterns and reports which AI provider received the data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khaney64](https://clawhub.ai/user/khaney64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to check local session JSONL logs for configured credential fragments and identify which external AI provider received a suspected leak. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session logs, which may contain sensitive conversation or credential material. <br>
Mitigation: Run it locally, restrict access to the generated report, and avoid sharing output that includes session identifiers or provider details unless needed for incident response. <br>
Risk: Storing full credentials in the leak-check configuration would create additional sensitive data at rest and can cause config echoes if discussed in a session. <br>
Mitigation: Store only partial credential fragments in the private config file and avoid reading or pasting that config during an OpenClaw session. <br>
Risk: The documented cleanup command deletes local session files when clearing config echoes. <br>
Mitigation: Confirm the exact session UUID before deleting any session log and keep backups when local history must be preserved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/khaney64/leak-check) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Leak check script](artifact/scripts/leak-check.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration guidance] <br>
**Output Format:** [Discord-style Markdown report by default, with optional JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports scanned file counts, checked credential counts, leak findings, config echoes, session identifiers, timestamps, providers, and models when available.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
