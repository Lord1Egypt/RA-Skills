## Description: <br>
A lightweight knowledge base and task-management skill that uses mixed JSON and Markdown storage for user profiling, task rhythm management, knowledge indexing, and daily knowledge-base evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WilliamTie](https://clawhub.ai/user/WilliamTie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to maintain a small to midsize local memory system with structured user-profile data, recurring task schedules, and indexed knowledge notes. It supports querying profile and task data, initializing a local workspace structure, and running a daily maintenance script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes persistent local memory and user-profile data. <br>
Mitigation: Review, edit, or reset data/user_profile.json before use, and avoid storing API keys or sensitive personal data in indexed memory files. <br>
Risk: The task rhythm configuration includes enabled recurring daily, weekly, and automated maintenance entries. <br>
Mitigation: Disable or adjust enabled entries in data/task_rhythm.json before use if recurring updates or deep-dialogue tasks are not desired. <br>
Risk: The maintenance script can update local knowledge-index and profile timestamps and create memory node directories in the configured workspace. <br>
Mitigation: Run the initialization and daily maintenance scripts only in an intended local workspace after reviewing their target paths. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/WilliamTie/lightweight-kb) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Communication Guide](artifact/references/communication.md) <br>
- [Task Execution Guide](artifact/references/task_guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local JSON profile, task rhythm, and knowledge-index files; query output may be plain text or formatted JSON when jq is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
