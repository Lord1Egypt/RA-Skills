## Description:

Read-only triage for a local git working tree that summarizes uncommitted changes and applies conservative risk flags before a commit, handoff, or local review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amitb-quantum](https://clawhub.ai/user/amitb-quantum)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get a compact, read-only summary of staged, unstaged, untracked, and conflicted local git changes with conservative risk flags before committing, handoff, or local review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The summary may reveal repository paths, filenames, git status, diff stats, and small capped samples of non-sensitive diffs.

Mitigation: Use it only in repositories where that level of local code visibility is acceptable, and keep secret-bearing files limited to filename-level inspection.

Risk: Conservative path- and filename-based risk flags can miss impacts that require full code review.

Mitigation: Treat the output as triage and run focused read-only checks or review before relying on it for important changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with ordered sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only git triage; deeper diff inspection is capped and secret-bearing filenames are reported without exposing values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
