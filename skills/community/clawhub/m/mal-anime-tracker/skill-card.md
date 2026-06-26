## Description: <br>
Track and manage MyAnimeList anime and manga lists, get anime details, rankings, seasonal updates, and receive new episode notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josetseph](https://clawhub.ai/user/josetseph) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and anime viewers use this skill to search MyAnimeList, inspect anime and manga lists, update anime status, remove list entries, refresh OAuth credentials, and produce notification text for new episode checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth tokens can grant access to MyAnimeList account data and list-management actions. <br>
Mitigation: Store tokens in OpenClaw vault or another secret manager, avoid sharing them in terminals or files, and rotate tokens if exposed. <br>
Risk: Update and delete commands can change or remove MyAnimeList entries. <br>
Mitigation: Double-check anime IDs and intended statuses before running list-changing commands, especially delete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/josetseph/mal-anime-tracker) <br>
- [MyAnimeList Developer Portal](https://myanimelist.net/apiconfig) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON or text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MyAnimeList OAuth credentials for account-specific commands.] <br>

## Skill Version(s): <br>
1.9.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
