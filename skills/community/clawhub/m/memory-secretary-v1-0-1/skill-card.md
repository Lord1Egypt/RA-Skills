## Description: <br>
Memory Secretary manages and analyzes local memory files with quality checks, duplicate-task detection, success-case extraction, work-pattern analysis, and reminder generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhm2084](https://clawhub.ai/user/yhm2084) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to inspect a workspace memory directory, find prior related work, summarize successful cases, and generate reminders or shareable status reports before starting new tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local workspace memory files and can write generated reports into the configured memory directory. <br>
Mitigation: Run it only against an intended workspace path and review generated reports before sharing them. <br>
Risk: The security guidance flags --force usage as needing review because it can overwrite local skill files. <br>
Mitigation: Review any --force install command before running it and confirm the artifact is the expected release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhm2084/memory-secretary-v1-0-1) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Python dictionaries and Markdown-oriented reports with example Python and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads workspace memory files and writes JSON reports under the configured memory/secretary directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and CHANGELOG.md, released 2026-04-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
