## Description:

Manage and retrieve long-term memories with LanceDB using semantic vector search, category filtering, and detailed metadata storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pntrivedy](https://clawhub.ai/user/pntrivedy)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add local long-term memory backed by LanceDB, then store, search, update, and retrieve memory records with metadata, categories, tags, and importance values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain caller-provided memory content on disk.

Mitigation: Review what data may be stored before installation, avoid sensitive content unless approved, and define retention and deletion practices before use.

Risk: The skill uses a fixed local storage path.

Mitigation: Confirm the storage path is appropriate for the deployment environment and update it before use when local policy or filesystem layout requires a different location.

Risk: The skill lacks built-in consent, redaction, retention, encryption, confirmation, and recovery controls.

Mitigation: Add or enforce these controls externally before using the skill in workflows that may process sensitive or regulated information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pntrivedy/skills/lancedb-memory)
- [Artifact SKILL.md](artifact/SKILL.md)
- [LanceDB memory implementation](artifact/lancedb_memory.py)
- [Final memory implementation](artifact/final_memory.py)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration instructions]

**Output Format:** [Markdown guidance and Python data structures returned by memory helper functions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory records may include caller-provided content, timestamps, categories, tags, importance values, and metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-01-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
