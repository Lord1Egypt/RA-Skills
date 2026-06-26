## Description: <br>
Create and manage fair-shuffled Padel Americano sessions, including player registration, round generation, score tracking, roster changes, leaderboards, and PDF exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reditya](https://clawhub.ai/user/reditya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Event organizers and agents use this skill to run Padel Americano tournaments or open-ended sessions, generate fair rotations, record scores, update rosters, rank players, and export schedules or standings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and modifies local tournament JSON files at paths provided by the user. <br>
Mitigation: Review output paths before running commands and keep tournament state files in an intended project or event directory. <br>
Risk: PDF export may launch local Chrome/Chromium with reduced sandboxing. <br>
Mitigation: Use trusted tournament data for exports and review the generated HTML or PDF output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reditya/padel-americano) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; local JSON tournament state; optional HTML or PDF reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. The CLI writes tournament state to user-provided paths and can export reports through local Chrome/Chromium when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
