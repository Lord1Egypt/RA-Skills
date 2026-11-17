## Description:

Provides fast Hong Kong MTR next-train ETA lookups with fuzzy station matching, multi-line support, and bilingual Traditional Chinese/English output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomfong](https://clawhub.ai/user/tomfong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Hong Kong transit questions by retrieving real-time MTR arrivals for stations or lines in English or Traditional Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to disclosed Hong Kong MTR and DATA GOV HK endpoints for live ETA and station data.

Mitigation: Confirm those endpoints are acceptable before installation and keep network access limited to opendata.mtr.com.hk and rt.data.gov.hk.

Risk: Refreshing station data writes a local CSV cache inside the skill directory.

Mitigation: Permit only the disclosed skill-local write scope, especially scripts/mtr_lines_and_stations.csv and scripts/__pycache__/.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomfong/skills/hk-mtr-next-train)
- [DATA GOV HK MTR train ETA endpoint](https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php)
- [MTR lines and stations CSV](https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise plain text or Markdown grouped by station, line, platform, destination, and ETA.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live transit data when available and a local station CSV cache for matching; the skill directs agents not to fabricate ETA values.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact changelog, released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
