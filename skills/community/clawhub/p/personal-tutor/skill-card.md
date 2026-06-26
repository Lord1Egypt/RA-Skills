## Description: <br>
Personal Tutor helps an AI agent run structured learning sessions, manage syllabi and learning logs, quiz the learner, and archive lesson concepts into a configured knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ben61405](https://clawhub.ai/user/ben61405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and agents use this skill to plan new subjects, continue daily lessons, check understanding with quizzes, and keep learning records, memory, and Markdown knowledge-base notes synchronized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write local learning records, knowledge-base notes, configuration, and memory or rule files. <br>
Mitigation: Restrict it to explicit learning and notes folders, require confirmation before writes, and review any edits to SOUL.md, TOOLS.md, MEMORY.md, or other persistent agent rule files. <br>
Risk: The skill may run local link-checking scripts after knowledge-base updates. <br>
Mitigation: Require user confirmation before script execution and inspect the script and working directory first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ben61405/personal-tutor) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Interactive tutoring prose, Markdown learning files, JSON configuration, and occasional shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local syllabus, learning-log, memory, index, and knowledge-base Markdown files according to user configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
