## Description:

Project Memory Ledger helps agents maintain a local-first engineering memory ledger with invariants, decisions, changes, evidence, rollback notes, and optional project document scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zcweah1981](https://clawhub.ai/user/zcweah1981)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to keep durable project memory across sessions, including project invariants, decision logs, change logs, traceability, rollback notes, and PRD patch proposals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says documented local-only behavior does not fully match the code, and some project names can steer writes outside intended locations.

Mitigation: Prefer backend=local, use a dedicated workspace path, review local_dir and projects_root_dir before use, and avoid untrusted project names.

Risk: The optional Drive backend can create or update Google Drive resources and the security guidance says Drive query escaping needs review.

Mitigation: Do not enable gws or Drive access until the local-only documentation mismatch, path containment, and Drive query escaping issues are fixed.

Risk: The authoritative security verdict is suspicious.

Mitigation: Review the code before installing, constrain where it can write, and run it with the least access needed for the selected backend.

## Reference(s):

- [Project Memory Ledger release page](https://clawhub.ai/zcweah1981/skills/project-memory-ledger)
- [default_config.json](artifact/references/default_config.json)
- [Ledger templates](artifact/references/ledger_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown ledger entries, JSON command output, configuration JSON, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown ledger files and, when configured for Drive, may create or update Google Drive documents through gws.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
