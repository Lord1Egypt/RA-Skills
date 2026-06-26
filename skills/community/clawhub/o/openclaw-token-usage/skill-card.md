## Description: <br>
Inspect token usage from local OpenClaw transcripts across a specified time range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujohn74](https://clawhub.ai/user/lujohn74) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect transcript-based token usage by time range, agent, provider, model, session, ranking, and export format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports and exports may reveal local usage patterns, model names, agent names, session identifiers, and other transcript metadata. <br>
Mitigation: Use narrow date ranges and filters when possible, and treat generated JSON, CSV, and Markdown reports as sensitive. <br>
Risk: Counts are transcript-based and may omit usage outside OpenClaw or transcript entries with no recorded token usage. <br>
Mitigation: State timezone and scope assumptions in summaries, and avoid presenting the report as complete billing or IDE-side GitHub Copilot usage data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lujohn74/openclaw-token-usage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV files, Shell commands, Guidance] <br>
**Output Format:** [Plain text summaries, Markdown reports, JSON, and CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript-based counts with date range, timezone, agent, provider, model, top-session, output-file, and CSV-directory options.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
