## Description: <br>
Little Steve Content Inbox helps agents save user-requested links, notes, and image paths into a local chat-oriented inbox, then list, view, star, mark, or delete entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EchoOfZion](https://clawhub.ai/user/EchoOfZion) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Chat users and their agents use this skill to explicitly archive links, notes, and image paths from conversation into a lightweight local inbox, then manage review status and pagination from the same chat workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved notes, links, tags, and local image paths are stored in the skill's local JSON data and may contain sensitive information if the user archives it. <br>
Mitigation: Only save content after clear user intent, avoid secrets or private local paths, and review or clear bundled inbox items before sharing or deployment. <br>
Risk: The skill runs local Bash scripts and depends on jq. <br>
Mitigation: Inspect the scripts before installation and run them only in a trusted local environment with jq installed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/EchoOfZion/little-steve-content-inbox) <br>
- [Publisher profile](https://clawhub.ai/user/EchoOfZion) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with local JSON-backed inbox state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq; stores user-approved links, notes, tags, statuses, and image paths in local JSON data.] <br>

## Skill Version(s): <br>
0.1.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
