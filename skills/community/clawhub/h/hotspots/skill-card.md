## Description: <br>
Fetches live hotspot and trending news data from the configured public API, ranks top items by model-estimated interest, summarizes them, and groups titles by source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xltang](https://clawhub.ai/user/xltang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve the latest hotspot/news items, check service reachability, view top summarized items, and group current titles by source. It can also provide an optional user-approved cron setup command for scheduled briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger terms such as "热点" may activate the skill when the user only intended a generic trend discussion. <br>
Mitigation: Confirm the user wants live hotspot/news retrieval before calling the API when intent is ambiguous. <br>
Risk: Optional scheduled briefings can create a persistent cron entry if the user approves setup. <br>
Mitigation: Do not create background tasks by default; provide the cron command only after explicit user confirmation. <br>
Risk: Live API results can be unavailable, malformed, or incomplete. <br>
Mitigation: Report explicit failure or degraded status, skip malformed items safely, and do not fabricate hotspot content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xltang/hotspots) <br>
- [Hotspot latest API endpoint](https://hotspot.api4claw.com/hotspots/latest?timestamp=$TIME_STEMP) <br>
- [Publisher profile](https://clawhub.ai/user/xltang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Concise Markdown with ranked lists, grouped titles, status text, and optional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Top results are capped at 10 items; scheduled setup is proposed only after user approval.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
