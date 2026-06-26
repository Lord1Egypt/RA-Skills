## Description: <br>
Huahua Dream helps an agent run scheduled memory organization and self-reflection by consolidating conversation memories, pruning stale notes, and summarizing behavior patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiye1997](https://clawhub.ai/user/baiye1997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give an agent a scheduled routine for reviewing past sessions, maintaining long-term memory files, and producing self-reflection notes. It is intended for environments where users can inspect and control memory updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read past conversation logs and persist inferred user memories or relationship notes. <br>
Mitigation: Review the generated sessionsPath, keep automatic writes disabled for a trial run, and confirm that stored memories can be inspected, rolled back, and deleted. <br>
Risk: Automatic memory edits may preserve incorrect or unwanted inferences. <br>
Mitigation: Inspect dream summaries and proposed memory changes before relying on them, especially after enabling scheduled execution or auto-approval. <br>


## Reference(s): <br>
- [Huahua Dream on ClawHub](https://clawhub.ai/baiye1997/huahua-dream) <br>
- [README](README.md) <br>
- [Memory Types Classification Guide](references/memory-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON script output, and memory file updates or proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update or propose updates to MEMORY.md, memory topic files, dream reports, and dream-config.json when authorized.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
