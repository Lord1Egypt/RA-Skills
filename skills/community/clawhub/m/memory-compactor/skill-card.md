## Description: <br>
Automatically organizes and compacts long-term memory by summarizing key points, deduplicating content, and removing stale information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soroyue](https://clawhub.ai/user/soroyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to compact persistent memory files into concise summaries, preserve important long-term information, and remove outdated temporary details. It is intended for memory maintenance workflows where proposed changes can be reviewed before they are applied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may be rewritten or removed without clear confirmation, preview, backup, or rollback safeguards. <br>
Mitigation: Use the skill manually, require a preview or diff before changes, and keep versioned backups before applying compaction. <br>
Risk: Scheduled or threshold-based cleanup could compact memory before retention rules and restore behavior are clear. <br>
Mitigation: Avoid scheduled or threshold-based cleanup until retention rules are defined and restore behavior has been tested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/soroyue/memory-compactor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance for memory compaction decisions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose summaries, deletions, and deduplication of persistent memory; require review before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
