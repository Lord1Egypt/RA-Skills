## Description: <br>
Analyze synced health data across Oura, Withings, Hevy, Strava, WHOOP, and Eight Sleep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[filipe-m-almeida](https://clawhub.ai/user/filipe-m-almeida) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to set up and query locally synced health data across supported providers, then summarize sleep, recovery, training, activity, and body-metric trends with practical guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data and provider credentials on the agent host. <br>
Mitigation: Install only if the health-sync npm package is trusted, protect workspace/health-sync/.health-sync.creds and health.sqlite, prefer the encrypted bootstrap flow, avoid raw secrets in chat, and remove local credentials and data when no longer needed. <br>
Risk: Health analysis can be misleading when local data is stale, incomplete, or provider sync fails. <br>
Mitigation: Run health-sync sync before analysis, report sync failures or data coverage limits clearly, and continue with stale data only when the user explicitly accepts that limitation. <br>
Risk: Provider schemas and API payloads differ across Oura, Withings, Hevy, Strava, WHOOP, and Eight Sleep. <br>
Mitigation: Consult the relevant provider schema reference before querying and explain uncertainty when fields, timestamps, or coverage do not support a confident answer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/filipe-m-almeida/health-sync) <br>
- [Health Sync setup reference](references/setup.md) <br>
- [Oura schema reference](references/oura.md) <br>
- [Withings schema reference](references/withings.md) <br>
- [Hevy schema reference](references/hevy.md) <br>
- [Strava schema reference](references/strava.md) <br>
- [WHOOP schema reference](references/whoop.md) <br>
- [Eight Sleep schema reference](references/eightsleep.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown answers with inline shell commands and SQL-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local health-sync CLI access and a synced SQLite cache; analysis should disclose stale or incomplete data.] <br>

## Skill Version(s): <br>
0.3.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
