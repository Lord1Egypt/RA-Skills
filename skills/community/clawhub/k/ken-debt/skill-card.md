## Description:

Harvest every ken: ceiling comment into one ledger, so brute-force deferrals get tracked instead of forgotten.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajnandan1](https://clawhub.ai/user/rajnandan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan a repository for `ken:` debt markers and produce a concise ledger of brute-force ceilings, upgrade triggers, and missing-trigger risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository scans can surface internal filenames, code comments, and technical debt details in the ledger output.

Mitigation: Review the generated ledger before sharing it outside the repository team.

Risk: Persisting the ledger creates a new repository file when the user explicitly asks for file output.

Mitigation: Confirm the target filename and review the generated file before committing it.

Risk: `ken:` markers without upgrade triggers can become stale deferrals.

Mitigation: Use the skill's `no-trigger` tagging and summary count to identify markers that need follow-up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rajnandan1/skills/ken-debt)
- [Project homepage](https://github.com/rajnandan1/ken)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown ledger with file, line, ceiling, upgrade trigger, tags, and summary counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and reports by default; can write a ledger file only when requested.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
