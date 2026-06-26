## Description: <br>
Access Granola meeting transcripts and notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scald](https://clawhub.ai/user/scald) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to sync Granola meeting history from a signed-in macOS desktop session into local files for review, search, and downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync script uses the user's signed-in Granola desktop session token to download meeting history. <br>
Mitigation: Install only when comfortable with this access pattern, keep the Granola desktop session under the intended user account, and review the script before running it. <br>
Risk: Synced transcripts, notes, attendee metadata, and raw document data may contain sensitive meeting information. <br>
Mitigation: Store the output directory in a protected location and avoid syncing it to untrusted backups, shared folders, or multi-user locations. <br>
Risk: Automated cron sync can continue downloading new meeting data in the background. <br>
Mitigation: Enable the cron job only when ongoing background updates are intended and disable it when continuous syncing is no longer needed. <br>


## Reference(s): <br>
- [Granola homepage](https://granola.ai) <br>
- [Granola API endpoint used by the sync script](https://api.granola.ai/v1) <br>
- [ClawHub skill page](https://clawhub.ai/scald/granola) <br>
- [Publisher profile](https://clawhub.ai/user/scald) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Local Markdown and JSON meeting files plus Markdown setup and search commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, macOS Granola desktop sign-in, and access to the local Granola auth file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
