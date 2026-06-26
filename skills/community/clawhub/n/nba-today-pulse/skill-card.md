## Description: <br>
Timezone-aware NBA daily intelligence using bundled public ESPN/NBA fetchers plus official NBA injury-report PDFs, with compact day fast path, same-day stats, phase-specific game routes, stronger single-game live detail, independent official-report summaries, refresh-safe follow-ups, and direct tool-output delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhjsnsnsk](https://clawhub.ai/user/hhjsnsnsk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to answer NBA daily status, stat leader, preview, live-flow, recap, injury-report, and official-report questions from public ESPN and NBA sources while keeping relative dates grounded in the requestor's timezone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound web requests and reads remote PDFs for NBA data, and server security evidence flags broader network and cache behavior than the package describes. <br>
Mitigation: Run it only in environments where NBA sports-data network access is acceptable, and restrict egress to ESPN and NBA hosts where possible. <br>
Risk: Official-report handling can process user-supplied URLs. <br>
Mitigation: Avoid passing non-NBA URLs to the official-report feature. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hhjsnsnsk/nba-today-pulse) <br>
- [Publisher profile](https://clawhub.ai/user/hhjsnsnsk) <br>
- [NBA.com official report URL example](https://www.nba.com/game/hou-vs-lal-0042500171) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or direct tool text with concise sports report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be bilingual and timezone-grounded; successful runs return the bundled tool output directly.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release metadata, README.md, SKILL.md, TOOLS.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
