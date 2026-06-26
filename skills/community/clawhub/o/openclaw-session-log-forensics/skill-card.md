## Description: <br>
Analyze OpenClaw session JSONL history for cost spikes, tool-call anomalies, and behavior regressions with jq + rg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators and developers use this skill to inspect local session logs during incident forensics, including cost spikes, tool-call anomalies, behavior regressions, and older conversation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes local session history that may contain secrets, private conversation content, or personal data. <br>
Mitigation: Scope searches narrowly, avoid sharing raw transcripts, and prefer redacted summaries or compact snapshots for incident notes. <br>
Risk: Broad searches across all sessions can expose more historical context than needed for the investigation. <br>
Mitigation: Use targeted dates, keywords, session IDs, and thresholds before expanding to all-session scans. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielsinewe/openclaw-session-log-forensics) <br>
- [Publisher profile](https://clawhub.ai/user/danielsinewe) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local forensic queries, summaries, anomaly shortlists, and compact per-session snapshots; does not require network output.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
