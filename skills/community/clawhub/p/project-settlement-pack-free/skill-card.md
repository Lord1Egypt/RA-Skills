## Description:

A local checker for construction and project settlement worksheets that runs 14 built-in checks per project directory and reports one conclusion line per project with source file and line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External project accountants, cost staff, construction managers, and owner-side project managers use this skill to check project settlement materials at recurring reporting, subcontract settlement, billing, collection, and fixed-asset transfer points. It helps identify calculation and consistency issues in submitted text materials, while leaving audit, legal, contract, and valuation decisions to qualified reviewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill output can be mistaken for an audit opinion, legal conclusion, or valuation decision.

Mitigation: Use the findings as calculation and consistency aids, then have qualified reviewers apply the contract terms, audit requirements, engineering cost rules, and approval process before acting.

Risk: A project may have checks or sub-checks marked not run when materials are incomplete or outside the free release scope.

Mitigation: Review every not-run item and material coverage warning before relying on the project conclusion; add the missing text materials and rerun when needed.

Risk: Settlement materials may contain sensitive commercial or financial data.

Mitigation: Run the checker only in an approved local environment and avoid sharing input materials or outputs outside the user's normal project review workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/project-settlement-pack-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Console text by default, with optional machine-readable JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite the project, check item, source file, line number, issue category, and relevant figures when the input materials support a conclusion.]

## Skill Version(s):

1.0.26 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
