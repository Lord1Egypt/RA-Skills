## Description:

Implement secure JWT authentication with proper validation, token lifecycle, and key management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as JWT security guidance when implementing authentication, token validation, token lifecycle controls, and key management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: JWT guidance can be misapplied when library defaults or token settings differ from the user's stack.

Mitigation: Verify algorithm allowlists, claim checks, key handling, and clock-skew settings against the selected JWT library before deployment.

Risk: Attack-test examples can affect systems if run without authorization.

Mitigation: Run validation checks and attack simulations only in owned or explicitly authorized environments.

## Reference(s):

- [JWT skill page](https://clawhub.ai/ivangdavila/skills/jwt)
- [Algorithm Traps](artifact/algorithms.md)
- [Common Attacks and Mitigations](artifact/attacks.md)
- [Token Lifecycle Traps](artifact/lifecycle.md)
- [Validation Traps](artifact/validation.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with implementation checklists and library-specific examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no commands or hidden execution behavior.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
