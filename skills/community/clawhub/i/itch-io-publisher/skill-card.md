## Description: <br>
Read itch.io creator stats and publish or update itch.io game builds from Windows using the itch.io server-side API and Butler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to validate an itch.io API key, inspect account and game stats, install Butler, and publish local game builds to itch.io channels. It is intended for Windows-based publishing workflows where the user confirms the source path and target project before upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an itch.io API key that can expose account data or authorize publishing actions if mishandled. <br>
Mitigation: Treat the API key as sensitive, avoid pasting it back into chat, and remove temporary credential files after Butler commands complete. <br>
Risk: A live Butler push can publish or update the wrong project, channel, or build if the source path or target is incorrect. <br>
Mitigation: Confirm the exact local source path and itch.io target before live upload, and use the dry-run path for new projects or channels. <br>
Risk: The workflow downloads the latest Windows Butler build from a remote endpoint. <br>
Mitigation: Independently verify the Butler download source when stricter supply-chain assurance is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stanestane/itch-io-publisher) <br>
- [itch.io API endpoint](https://itch.io/api/1/$key) <br>
- [Butler Windows download endpoint](https://broth.itch.zone/butler/windows-amd64/LATEST/archive/default) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with PowerShell command blocks and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Windows PowerShell commands for itch.io API calls, Butler installation, dry-run pushes, and live pushes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
