## Description: <br>
Leexi (leexi.ai). Use this skill for ANY Leexi request - searching and reading data. Whenever a task involves Leexi, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search and read calls, meetings, call notes, teams, and users from a Leexi workspace through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connector responses can include sensitive Leexi workspace information such as calls, meeting notes, team data, and user lists. <br>
Mitigation: Treat returned data as sensitive and share it only with users who are authorized to access the relevant Leexi workspace. <br>
Risk: Future connector actions may write, overwrite, or remove Leexi data. <br>
Mitigation: Approve write or destructive actions only after reviewing the exact payload, target, and expected effect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-leexi) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Leexi homepage](https://www.leexi.ai/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Leexi workspace data from connector calls, including calls, meeting notes, teams, and users.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
