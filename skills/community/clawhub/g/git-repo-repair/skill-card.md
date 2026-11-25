## Description:

Repair a broken git repository: bad object HEAD, broken ref chains, committing working-tree changes. Backup, rebuild refs and index, then resurrect commits. Produces HEAD + fsck/status verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to diagnose and locally repair broken Git references or missing objects, recover commits, and verify the resulting repository state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this skill suspicious because it reports deletion of the Git index despite a stated no-deletion boundary, and coverage is partial.

Mitigation: Review the skill’s backup and index-rebuild steps before installing, especially how they handle backup failure and preserve staged work.

Risk: Two local references were missing from the scan, so the available results do not establish that all referenced material was assessed.

Mitigation: Review the referenced material before relying on the procedure.

## Reference(s):

- [ClawHub release](https://clawhub.ai/zuoyunlai/skills/git-repo-repair)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with shell commands and a recovery verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recovery steps, HEAD hash comparison, fsck/status/log evidence, working-tree status, and a list of irreversible actions not taken.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
