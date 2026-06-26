## Description: <br>
Garmin Connect integration for Clawdbot: sync fitness data (steps, HR, calories, workouts, sleep) every 5 minutes using OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovefromio](https://clawhub.ai/user/lovefromio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to authenticate with Garmin Connect, sync fitness and health metrics into a local Clawdbot cache, and format those metrics for scripts or agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to pass Garmin account credentials to an authentication script, and server security guidance warns against command-line password handling and disabling 2FA. <br>
Mitigation: Use a safer OAuth flow or edit the scripts before use; do not pass your Garmin password on the command line or disable 2FA. <br>
Risk: Garmin OAuth sessions and detailed health data are stored locally in files such as ~/.garth/session.json and cache JSON files. <br>
Mitigation: Protect local session and cache files, restrict file permissions, and install only if local storage of Garmin health and session data is acceptable. <br>
Risk: Some scripts include hard-coded personal paths, a personal email, and /tmp export or dashboard behavior. <br>
Mitigation: Remove personal values and avoid /tmp export or dashboard scripts unless local plaintext health-data exposure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lovefromio/lovefromio-garmin-connect) <br>
- [Garmin OAuth sign-in](https://sso.garmin.com/sso/signin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python usage examples, and JSON fitness data output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Garmin session and cache files; formatted summaries may include detailed health and workout data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
