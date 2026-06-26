## Description: <br>
Organizes movie recommendations in Obsidian and generates suggestions based on user profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adnxone](https://clawhub.ai/user/adnxone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal productivity agents use this skill to organize movie recommendations in an Obsidian vault, maintain watchlist and seen files, and generate profile-based suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, move, and update files in an Obsidian Movies area. <br>
Mitigation: Configure the Movies paths carefully and review proposed file moves, index updates, and profile changes before accepting them. <br>
Risk: Recommendation context may include personal taste, journal, or mood information if the agent is allowed to inspect it. <br>
Mitigation: Do not allow access to unrelated journals or mood logs unless that context is explicitly intended for movie recommendations. <br>
Risk: Unreleased movie handling may propose a cron reminder. <br>
Mitigation: Approve any cron reminder before it is created. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adnxone/movie-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes and concise guidance with optional shell commands for reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates Obsidian movie note files, indexes, profile notes, and optional cron reminders when approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
