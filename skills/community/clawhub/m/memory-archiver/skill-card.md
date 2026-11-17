## Description:

Memory Archiver helps OpenClaw agents maintain local daily, weekly, and long-term memory with automatic search, extraction, session notes, and consolidation hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amd5](https://clawhub.ai/user/amd5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to persist useful conversation context, search prior memory, and consolidate local notes across sessions. It is suited for agents that need continuity over repeated work in a local workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically persists conversation content in local memory and session note files, which can retain sensitive prompt content.

Mitigation: Install only when local conversation memory is desired, review stored memory files regularly, and remove sensitive entries from the workspace memory directories.

Risk: Persistent hooks and scheduled jobs can bring old memory back into future conversations without strong user controls.

Mitigation: Review the installed hooks and cron jobs after installation, disable them when continuous memory is not needed, and clean generated memory files before sensitive work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amd5/skills/memory-archiver)
- [Publisher Profile](https://clawhub.ai/user/amd5)
- [Memory Archiver Skill Documentation](artifact/SKILL.md)
- [Memory Management Script Documentation](artifact/scripts/README.md)
- [Memory Consolidation Prompt](artifact/prompts/consolidation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, local memory files, hook output, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local OpenClaw workspace memory, session, hook, and cron-related files.]

## Skill Version(s):

10.3.0 (source: frontmatter, skill.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
