## Description:

Use TPSCheck to check UK phone numbers against TPS and CTPS, run batch checks, or retrieve account credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to check individual or batches of UK phone numbers against TPS and CTPS, and to view TPSCheck account credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unchecked downloaded code.

Mitigation: Review and approve the CLI installation separately before allowing setup.

Risk: Startup synchronization can install additional agent skills persistently.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Phone numbers are shared with OOMOL and TPSCheck when checked.

Mitigation: Submit only phone numbers you intend to share with those services.

## Reference(s):

- [TPSCheck API documentation](https://www.tpscheck.uk/documentation/)
- [TPSCheck homepage](https://www.tpscheck.uk)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Natural-language summaries and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Phone-check results for individual numbers or batches of up to 100; account credit and plan details.]

## Skill Version(s):

1.0.6 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
