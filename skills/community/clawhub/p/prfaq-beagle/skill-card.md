## Description:

Use when the user wants to pressure-test a product, internal-tool, or OSS concept against Amazon's Working Backwards PRFAQ gauntlet before committing to a spec.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Product builders, internal-tool owners, and open-source maintainers use this skill to pressure-test an idea through a gated PRFAQ process before committing to specification or implementation work. It produces a binary pass/fail verdict and, on pass, a concept brief for downstream brainstorming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update .beagle concept files using a user-selected slug.

Mitigation: Use a simple lowercase hyphenated slug without slashes or path-like segments, and review generated paths before allowing writes or refreshes.

Risk: Automatic local artifact analysis may scan more planning or documentation files than a user expects.

Mitigation: Install and run the skill only when local project-document scanning is acceptable, and review the planned analysis scope before proceeding.

Risk: The workflow may invoke web research and incorporate externally sourced findings into product validation.

Mitigation: Review research outputs before relying on them for a pass/fail product decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/prfaq-beagle)
- [Companion Invocation Contract](references/companion-contract.md)
- [PRFAQ Document Template](references/prfaq-template.md)
- [Press Release Stage](references/press-release.md)
- [Customer FAQ Stage](references/customer-faq.md)
- [Internal FAQ Stage](references/internal-faq.md)
- [Verdict and Brief Stage](references/verdict.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with generated PRFAQ and concept brief files when the concept passes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not produce code, implementation plans, or polished specifications.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
