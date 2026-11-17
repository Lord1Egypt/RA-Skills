## Description:

Reviews Rust macro code for hygiene issues, fragment misuse, compile-time impact, and procedural macro patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Rust declarative and procedural macros for correctness, hygiene, diagnostics, compile-time impact, and edition-specific risks before reporting code-review findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A macro review may require the agent to read Rust project files in the active workspace.

Mitigation: Run the review only in the intended project workspace and avoid including unrelated sensitive files in scope.

Risk: One reporting gate depends on a separate review-verification-protocol skill.

Mitigation: Ensure that companion skill is available, or perform equivalent macro-specific verification before reporting findings.

Risk: Incomplete crate context or partial macro-definition review can lead to incorrect findings.

Mitigation: Follow the skill's gates: inspect Cargo.toml, read full macro definitions, and cite current-tree file and line evidence for every issue.

## Reference(s):

- [Declarative Macros](references/declarative-macros.md)
- [Procedural Macros](references/procedural-macros.md)
- [ClawHub skill page](https://clawhub.ai/anderskev/skills/macros-code-review)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown code-review findings with file and line references, severity labels, and concise explanations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are gated on crate-context review, complete macro-definition reading, current-tree file and line evidence, and a separate review-verification protocol.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
