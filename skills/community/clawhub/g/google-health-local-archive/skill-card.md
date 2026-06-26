## Description: <br>
Read a local ghcli archive of Google Health API data for Fitbit/Google health accounts. Uses read-only local JSON queries and never calls Google Health directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdsouvenir](https://clawhub.ai/user/fdsouvenir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer health, activity, sleep, heart, body, and device/source questions from a local ghcli Google Health/Fitbit archive while keeping archive access read-only and date-bounded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent query sensitive local health archive data. <br>
Mitigation: Keep queries date-bounded, use ghcli read-only flags for archive access, and avoid dumping broad archive contents. <br>
Risk: Setup, login, sync, or export commands can change credentials, refresh local data, or expose archive contents. <br>
Mitigation: Approve those commands only when the user explicitly asks for that action. <br>
Risk: Health data may be stale or incomplete and could be misread as medical advice. <br>
Mitigation: Mention data freshness when relevant and do not make medical claims or diagnoses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fdsouvenir/google-health-local-archive) <br>
- [Publisher profile](https://clawhub.ai/user/fdsouvenir) <br>
- [ghcli project](https://github.com/fdsouvenir/ghcli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and summarized local JSON query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only ghcli queries should be date-bounded; setup, login, sync, and export commands are proposed or run only after explicit user request.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
