## Description:

A free local checker for owner-supplied material ledgers that recomputes issued quantity, issued amount, and settlement deduction amounts row by row, cross-checks totals, and flags duplicate rows, blanks, and negative values with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Project cost staff, subcontractor settlement reviewers, and construction operations teams use this skill during monthly progress measurement and final settlement to check owner-supplied material ledgers before payment deductions are finalized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake a clean free-version result for coverage of checks that the release explicitly withholds, such as over-issue deductions, return-not-offset detection, contract-price mismatch, or missed deductions.

Mitigation: Treat results as limited to the disclosed free checks and review withheld checks separately or with a tool that explicitly performs them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/owner-supplied-material-check-free)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Human-readable text or JSON findings with source ledger line references and missing-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided ledger text; insufficient input produces missing-field guidance instead of a clean-result conclusion.]

## Skill Version(s):

1.0.51 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
