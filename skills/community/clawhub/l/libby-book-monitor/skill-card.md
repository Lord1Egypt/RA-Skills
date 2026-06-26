## Description: <br>
Track book availability on Libby/OverDrive libraries, search library catalogues, manage a watchlist, and get notified when books are added. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexpolonsky](https://clawhub.ai/user/alexpolonsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to search Libby/OverDrive catalogues, maintain local book watchlists, and check whether watched books have appeared in a selected library collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Book titles, authors, and library codes used in searches are sent to OverDrive's catalog API. <br>
Mitigation: Use the skill only for reading-list data you are comfortable sending to OverDrive, and avoid adding sensitive titles to watched searches. <br>
Risk: The watchlist and default library configuration are stored locally in the configured data directory. <br>
Mitigation: Choose a data directory with appropriate local file permissions, and remove stored watchlists when they are no longer needed. <br>
Risk: Recurring checks or notification integrations can persist outside the skill itself. <br>
Mitigation: Document any cron job, scheduler entry, or notification destination created for this skill so it can be audited or disabled later. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexpolonsky/libby-book-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/alexpolonsky) <br>
- [OverDrive](https://www.overdrive.com/) <br>
- [OverDrive Thunder API](https://thunder.api.overdrive.com/v2/libraries) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands and local JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local watchlist and configuration JSON files under the configured data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
