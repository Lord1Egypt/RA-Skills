## Description:

Organizes, compresses, and curates OpenClaw memory by keeping MEMORY.md focused on durable long-term facts and preserving daily details in dated memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024)

### License/Terms of Use:


## Use Case:

External users and developers working in OpenClaw use this skill to scan, compress, clean, and selectively merge memory notes while keeping durable facts in MEMORY.md and daily history in dated files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File safety checks can be bypassed in untrusted workspaces where other users or archives can introduce symlinks.

Mitigation: Use the skill only in a trusted OpenClaw workspace and avoid running it in shared or archive-derived memory directories.

Risk: Compress, discard, or clean actions can permanently alter or delete memory data.

Mitigation: Back up MEMORY.md and the memory directory before destructive actions, and do not run clean until backups and discarded files are no longer needed.

Risk: The documented npx installer command is unpinned.

Mitigation: Prefer a pinned or verified installer command before installation.

## Reference(s):

- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [ClawHub skill page](https://clawhub.ai/codeblackhole1024/skills/memory-organizer)
- [Publisher profile](https://clawhub.ai/user/codeblackhole1024)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide changes to OpenClaw memory files; review destructive actions before execution.]

## Skill Version(s):

1.2.1 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
