## Description: <br>
Track rounds, handicap, clubs, and courses with personalized improvement tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to keep a local golf log, track rounds, handicap, clubs, and courses, and receive personalized practice recommendations based on their history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update files under ~/golf/, which can affect existing golf notes in that folder. <br>
Mitigation: Review ~/golf/ before first use and keep backups of memory.md, rounds.md, courses.md, and archived season files if that folder already exists. <br>
Risk: Golf rules and handicap guidance may not match a user's current league, course, or tournament requirements. <br>
Mitigation: Confirm formal rulings and handicap calculations with the relevant golf association, course, or tournament authority before relying on them for official play. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/golf) <br>
- [Skill homepage](https://clawic.com/skills/golf) <br>
- [Clubs Guide](artifact/clubs.md) <br>
- [Memory Setup](artifact/memory-template.md) <br>
- [Rules Reference](artifact/rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local Markdown file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local Markdown files under ~/golf/ for round history, course notes, club distances, and handicap summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
