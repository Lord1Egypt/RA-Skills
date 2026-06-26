## Description: <br>
Audits OpenClaw runtime health before helping optimize inference speed and token usage through approval-gated audit, remediation, and cleanup workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vitalyis](https://clawhub.ai/user/vitalyis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw runtime health, verify command wiring and allowlist coverage, clean stale sessions, and apply inference-tuning changes only after review and approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can persistently modify agent command wiring and execution permissions. <br>
Mitigation: Run setup in preview mode first, inspect the path-specific approval entries, and use --apply only after review. <br>
Risk: Session and memory cleanup can remove operational history or user context. <br>
Mitigation: Use the default archive-first purge behavior and reserve --delete for cases where the exact removal set has already been verified. <br>
Risk: Preflight backups may contain sensitive OpenClaw state or workspace data. <br>
Mitigation: Keep generated backups protected and avoid sharing logs or examples that include secrets; use redacted placeholders when needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/vitalyis/inference-optimizer) <br>
- [Repository](https://github.com/vitalyis/inference-optimizer) <br>
- [README](artifact/README.md) <br>
- [Security notes](artifact/SECURITY.md) <br>
- [Release notes 0.3.4](artifact/docs/release-notes/0.3.4.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Approval-gated operational guidance; setup preview and archive-first cleanup are documented for sensitive state.] <br>

## Skill Version(s): <br>
0.3.4 (source: server release metadata, SKILL.md metadata, CHANGELOG released 2026-04-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
