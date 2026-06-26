## Description: <br>
Manage Things 3 via the `things` CLI on macOS, including adding or updating projects and todos through the URL scheme and reading, searching, or listing items from the local Things database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users on macOS use this skill to let an agent inspect Things 3 lists and search results, then prepare or execute task and project updates with the `things` CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require broad local access to read the Things 3 database. <br>
Mitigation: Grant Full Disk Access only to trusted calling apps and review requested local reads before relying on their results. <br>
Risk: Update commands can change or complete Things 3 tasks and may require a Things auth token. <br>
Mitigation: Use dry-run or manual confirmation before changes, and keep auth tokens in environment variables rather than prompts or command flags. <br>
Risk: The documented install command uses an unpinned third-party CLI release. <br>
Mitigation: Prefer a trusted pinned `things3-cli` version and verify the upstream project before installation. <br>


## Reference(s): <br>
- [MH things-mac on ClawHub](https://clawhub.ai/mohdalhashemi98-hue/mh-things-mac) <br>
- [things3-cli](https://github.com/ossianhempel/things3-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local Things 3 read results, dry-run command previews, and commands that modify or complete tasks when the user has granted access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
