## Description: <br>
Guides an agent through configuring and running OnelapSyncStrava to sync Onelap cycling activities to Strava. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kermit-r-wood](https://clawhub.ai/user/kermit-r-wood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up OnelapSyncStrava, configure Onelap and Strava credentials, complete Strava OAuth authorization, and run activity sync commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow relies on a third-party sync binary that can access Onelap account credentials and Strava upload authorization. <br>
Mitigation: Install only if comfortable with that access, prefer building from source or verifying the release, and revoke or rotate credentials if exposure is suspected. <br>
Risk: The local config.json contains Onelap credentials, Strava API credentials, and OAuth tokens. <br>
Mitigation: Keep config.json local with restrictive permissions and do not commit, paste, or share it. <br>
Risk: Incorrect configuration can cause failed authorization or failed sync attempts. <br>
Mitigation: Run the status and check commands before syncing, then review the reported result after sync completes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kermit-r-wood/onelap-sync-strava) <br>
- [OnelapSyncStrava releases](https://github.com/kermit-r-wood/OnelapSyncStrava/releases) <br>
- [OnelapSyncStrava build artifacts](https://github.com/kermit-r-wood/OnelapSyncStrava/actions/workflows/binaries.yml) <br>
- [Strava API settings](https://www.strava.com/settings/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include credential setup, OAuth authorization, status checks, and sync command guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
