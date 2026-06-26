## Description: <br>
Your personal movie assistant. Track what you watch, check your lists, and get movie info from Letterboxd instantly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tamil-9421](https://clawhub.ai/user/tamil-9421) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to retrieve public Letterboxd profile statistics, recent diary entries, watchlists, and movie details for supplied usernames or movie slugs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can display public Letterboxd activity for any supplied username. <br>
Mitigation: Confirm the intended Letterboxd username and account context before requesting or sharing profile, diary, or watchlist output. <br>
Risk: The Python dependency is declared without a pinned version. <br>
Mitigation: Review and pin an approved `letterboxdpy` version before installing or deploying the skill in a controlled environment. <br>
Risk: Recent diary output hardcodes the year in returned dates. <br>
Mitigation: Treat diary dates as approximate and confirm against Letterboxd before using them for records or decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tamil-9421/letterboxd-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/tamil-9421) <br>
- [Letterboxd](https://letterboxd.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON or plain text returned from Python command-line helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public Letterboxd lookups for a supplied username, diary limit, watchlist limit, or movie slug.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and README report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
