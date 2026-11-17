## Description:

Defines a capped LYGO living-memory index and provides local audit and compression helpers for continuity files, fragile item review, and optional minting preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a small LYGO/LYRA continuity index, audit missing or fragile memory items, and prepare a concise Master Archive only after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit and compression helpers inspect local paths under the selected LYGO_AUTHORITY_ROOT and can write local report or archive files.

Mitigation: Use a deliberately chosen authority root, inspect core_files_index.json for absolute paths, traversal, and symlinks, and run only in an intended local workspace.

Risk: A Master Archive or public anchor can expose secrets, personal data, or private conversation content if sensitive memory items are included.

Mitigation: Review FRAGILE items and remove API keys, wallet seeds, tokens, personal data, and private conversation content before minting or publishing any archive.

Risk: Installer or verifier drift can change what is installed or validated for a memory-sensitive workflow.

Mitigation: Use pinned ClawHub installer, skill, and verifier versions before running audit, compression, or minting steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lygo-universal-living-memory-library)
- [Metadata GitHub link](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Library Spec](references/library_spec.md)
- [Core Files Index](references/core_files_index.json)
- [Audit Protocol](references/audit_protocol.md)
- [Compression Protocol](references/compression_protocol.md)
- [Security Guidance](references/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown and terminal text with optional JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local audit report and MASTER_ARCHIVE.md when the bundled scripts are run.]

## Skill Version(s):

1.2.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
