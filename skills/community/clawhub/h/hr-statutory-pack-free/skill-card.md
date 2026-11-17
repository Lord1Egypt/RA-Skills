## Description:

Checks user-provided HR statutory cost materials locally for disability employment fund, union funds, and welfare and education expense caps, producing per-entity conclusions with source citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

HR and finance shared-service teams use this skill before statutory HR cost review cycles to check one or more entity material sets for arithmetic and reconciliation issues across three built-in checks. It is intended as a local review aid, not as legal, tax, audit, filing, or attestation advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads HR and finance materials supplied by the user.

Mitigation: Run it only with materials you are comfortable processing locally, and avoid passing unrelated sensitive files.

Risk: A clean result can be misread as legal, tax, audit, filing, or attestation advice.

Mitigation: Treat results as arithmetic and reconciliation support, and have qualified reviewers make legal, tax, audit, and filing decisions.

Risk: Some checks and sub-checks are explicitly not run in the free release.

Mitigation: Review checks_not_run and sub_checks_not_run before relying on a result, especially for cross-entity summaries and policy-specific judgments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/hr-statutory-pack-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON written to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each conclusion cites the relevant entity, check, source file, and line when findings are available; the skill does not write output files.]

## Skill Version(s):

1.0.21 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
