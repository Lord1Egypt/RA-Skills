## Description: <br>
Syncs daily health and fitness data from Oura Ring into markdown files. Provides sleep, readiness, activity, heart rate, stress, SpO2, and workout data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freakyflow](https://clawhub.ai/user/freakyflow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to sync Oura Ring health data into local daily markdown files so sleep, readiness, activity, stress, heart rate, SpO2, and workout data can be referenced later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Oura Ring health data is written as local plaintext markdown. <br>
Mitigation: Keep the output directory private and avoid committing or syncing generated health files unintentionally. <br>
Risk: The OURA_TOKEN secret could expose access to Oura data if leaked. <br>
Mitigation: Store OURA_TOKEN as a protected secret and revoke the token if it is exposed. <br>
Risk: Scheduled syncs can continue collecting fresh health data automatically. <br>
Mitigation: Enable cron only when ongoing automatic syncing is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freakyflow/oura-ring) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [Oura personal access tokens](https://cloud.ouraring.com/personal-access-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with concise setup and sync commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one local health markdown file per synced day when data is available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
