## Description: <br>
Provides Hong Kong MTR next-train ETA lookup with fuzzy station matching, multi-line support, and bilingual Traditional Chinese/English output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomfong](https://clawhub.ai/user/tomfong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and transit-focused agents use this skill to answer Hong Kong MTR arrival-time questions, including station-only, station-and-line, and multi-station ETA requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public Hong Kong transit-data endpoints and depends on their availability and freshness. <br>
Mitigation: Use the returned ETA data only for transit lookup responses, and present service-hour or no-information fallbacks when the public API has no result. <br>
Risk: The station dictionary can be refreshed by writing a CSV file inside the skill directory. <br>
Mitigation: Limit refreshes to the documented station-list CSV path and run the sync command only when installation or station-data updates require it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomfong/hk-mtr-next-train) <br>
- [MTR Trains ETA API](https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php) <br>
- [MTR lines and stations CSV](https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown or plain text with bilingual ETA summaries and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should not fabricate ETA values; live results depend on public Hong Kong transit-data endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill changelog, released 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
