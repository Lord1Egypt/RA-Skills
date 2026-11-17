## Description:

Generate MD5 and SHA checksums, verify integrity, and compare hash values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to compute hashes, verify downloaded files, compare file integrity, and check checksum manifests from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local history and batch manifest files can record file paths and hashes, which may reveal private project structure.

Mitigation: Avoid batch mode on sensitive directories unless a saved manifest is intended, and delete history or manifest files afterward when they expose private paths.

## Reference(s):

- [Hash on ClawHub](https://clawhub.ai/bytesagain-lab/skills/hash)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text command output and checksum manifest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch mode and history operations can write local records under ~/.local/share/hash.]

## Skill Version(s):

3.0.1 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
