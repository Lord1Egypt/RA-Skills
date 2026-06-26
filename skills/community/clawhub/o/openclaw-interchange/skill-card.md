## Description: <br>
Shared .md interchange library for OpenClaw skills - atomic writes, deterministic serialization, YAML frontmatter, advisory locking, and schema validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frank-bot07](https://clawhub.ai/user/frank-bot07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this library to read, write, validate, index, and reconcile Markdown interchange files shared across OpenClaw skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file writes and arbitrary file paths can affect files outside the intended interchange workspace. <br>
Mitigation: Set INTERCHANGE_ROOT to a dedicated directory, avoid untrusted file paths, and run the skill with least filesystem privilege. <br>
Risk: Advisory locking and stale-lock handling may be unsuitable for sensitive or high-concurrency workflows. <br>
Mitigation: Avoid high-concurrency production use until locking and path containment are reviewed or patched. <br>
Risk: The security verdict is suspicious because the file-write and locking design needs review before use. <br>
Mitigation: Audit the source and apply local patches before installing in workflows that handle important or sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frank-bot07/openclaw-interchange) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Security review](artifact/CODEX_REVIEW.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, JavaScript API results, and validation metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem I/O; callers can set INTERCHANGE_ROOT to isolate interchange files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
