## Description: <br>
Fetches Weibo hotspot data from hotspot.api4claw.com, groups titles by source_name, and can provide a user-approved OpenClaw cron command for daily updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xltang](https://clawhub.ai/user/xltang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to retrieve current Weibo hotspot titles, check hotspot service status, and display results grouped by source_name. It can also generate an optional OpenClaw cron registration command after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends timestamped requests to hotspot.api4claw.com. <br>
Mitigation: Install only if you trust that service to receive the requests. <br>
Risk: Optional daily cron setup can create automated polling if approved. <br>
Mitigation: Keep scheduled updates disabled unless wanted, and review any generated cron command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xltang/hotspots-weibo) <br>
- [Hotspot API base URL](https://hotspot.api4claw.com) <br>
- [Weibo hotspot endpoint](https://hotspot.api4claw.com/hotspots/platform/微博?timestamp=$TIME_STEMP) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown with grouped hotspot titles, status messages, and optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a fresh minute-precision timestamp for each API request and avoids displaying fetched_at or data_date fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
