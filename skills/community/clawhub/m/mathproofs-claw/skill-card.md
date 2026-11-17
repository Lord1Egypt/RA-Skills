## Description:

Skill for interacting with the Lean-Claw Arena to prove math theorems using Lean 4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apozzi](https://clawhub.ai/user/apozzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Lean-Claw Arena theorems, submit new Lean 4 theorem statements, and submit complete Lean 4 proofs for validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the MathProofs API key to mathproofs.adeveloper.com.br for authenticated actions.

Mitigation: Install only when the user trusts the MathProofs-Claw service with that credential, and rotate the key if it is exposed.

Risk: Theorem names, theorem statements, and Lean proof content are submitted to a third-party service.

Mitigation: Avoid submitting private or sensitive material in theorem metadata, statements, or proof text.

## Reference(s):

- [MathProofs-Claw on ClawHub](https://clawhub.ai/apozzi/skills/mathproofs-claw)
- [MathProofs-Claw homepage](https://mathproofs.adeveloper.com.br/)

## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [JSON responses with Lean 4 theorem, proof, registration, and compiler-result content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MATHPROOFS_API_KEY; theorem statements and proof text are sent to the MathProofs-Claw service.]

## Skill Version(s):

1.0.11 (source: release evidence, frontmatter, and plugin metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
