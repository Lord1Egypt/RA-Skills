## Description:

Micro Memory is a local agent memory tool for adding, searching, linking, reviewing, exporting, compressing, and reporting on persistent personal memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[payne-openclaw](https://clawhub.ai/user/payne-openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use Micro Memory to persist personal notes as local memories, search and link them, track strength decay, schedule reviews, and generate health reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores personal memory data in local plaintext files, Markdown backups, archives, and exports.

Mitigation: Avoid storing secrets or highly sensitive personal data, restrict access to the store directory, and review exported or archived files before sharing.

Risk: Broad automatic triggers may persist content more often than intended.

Mitigation: Prefer explicit memory commands for sensitive workflows and review new memories before relying on them.

Risk: The artifact ships a broken package manifest and an unsafe alternate command launcher.

Mitigation: Fix the package manifest before installation and use only the declared dist/index.js entry point; avoid bin/memory.js.

Risk: CSV exports can be unsafe when memory content comes from other people.

Mitigation: Treat CSV exports as untrusted, review or sanitize them before opening in spreadsheet software, and prefer JSON for interchange when possible.

## Reference(s):

- [Micro Memory ClawHub Skill Page](https://clawhub.ai/payne-openclaw/skills/micro-memory)
- [Artifact README](artifact/README.md)
- [Validation Plan](artifact/VALIDATION_PLAN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Terminal text and Markdown, with JSON or CSV file output for stored memories and exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local memory data in JSON and Markdown under store/ and may write archive or export files.]

## Skill Version(s):

4.0.2 (source: server release metadata; package.json text agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
