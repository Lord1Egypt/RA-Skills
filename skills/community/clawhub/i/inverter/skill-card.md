## Description:

Inverter and VFD parameter calculator. Use when json inverter tasks, csv inverter tasks, checking inverter status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to inspect and run the bundled command wrapper for inverter-related status, local entries, search, export, statistics, and configuration. Security evidence says it should not be relied on as an inverter/VFD calculator or real status checker until corrected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised inverter/VFD calculator purpose does not match the inspected local data-store behavior.

Mitigation: Review the artifact before installation and do not rely on it for inverter calculations or real equipment status checks until the behavior is corrected.

Risk: The skill stores, exports, and deletes local entries under the configured data directory.

Mitigation: Use a dedicated INVERTER_DIR, avoid storing sensitive values, and review exported files before sharing.

Risk: Security guidance identifies an unsafe config command plus sed and serialization issues.

Mitigation: Fix configuration update handling and data serialization before normal use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/inverter)
- [BytesAgain Homepage](https://bytesagain.com)
- [BytesAgain Publisher Profile](https://clawhub.ai/user/bytesagain-lab)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and Markdown command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local data directory configured by INVERTER_DIR; default is ~/.inverter/.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
