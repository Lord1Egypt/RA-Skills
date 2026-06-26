## Description: <br>
Query Plausible Analytics API for traffic stats, referrers, conversions, and custom events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Website owners, marketers, developers, and support agents use this skill to answer traffic, referrer, conversion, and custom-event questions from Plausible Analytics. It helps the agent prepare Plausible API queries, interpret common metrics, and retain non-secret site preferences locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent sends site IDs, analytics query parameters, and the Plausible API key to Plausible or a configured self-hosted Plausible instance. <br>
Mitigation: Install only when that data sharing is acceptable, use a scoped Plausible API key where possible, and keep the key in PLAUSIBLE_API_KEY rather than chat or skill files. <br>
Risk: The skill can retain tracked domains, goals, events, preferences, and cached query context under ~/plausible/. <br>
Mitigation: Review or delete ~/plausible/memory.md and saved query context when local retention is not desired. <br>


## Reference(s): <br>
- [ClawHub Plausible skill page](https://clawhub.ai/ivangdavila/plausible) <br>
- [Plausible skill homepage](https://clawic.com/skills/plausible) <br>
- [Plausible realtime visitors API endpoint](https://plausible.io/api/v1/stats/realtime/visitors) <br>
- [Plausible aggregate stats API endpoint](https://plausible.io/api/v1/stats/aggregate) <br>
- [Plausible timeseries stats API endpoint](https://plausible.io/api/v1/stats/timeseries) <br>
- [Plausible breakdown stats API endpoint](https://plausible.io/api/v1/stats/breakdown) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or concise text with Plausible query parameters and analytics summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PLAUSIBLE_API_KEY and may use ~/plausible/ for non-secret site preferences and cached query context.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
