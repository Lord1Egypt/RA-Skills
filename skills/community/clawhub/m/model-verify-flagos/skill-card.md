## Description:

Verify a user-specified target model by running serving checks with FlagGems and FlagCX disabled and then enabled, diffing the results to identify model, serving, or multi-chip stack failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate whether a target model can run on the base serving stack and on the full FlagGems/FlagCX multi-chip stack. It helps isolate model-specific failures from stack-specific failures and recommends the stack to use next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download user-selected remote models and run trusted custom model code inside Docker.

Mitigation: Install and run it only in a disposable, tightly scoped container with no secrets, no sensitive host mounts, and trusted or pinned model sources; review or remove --trust-remote-code unless required.

Risk: Verification commands run against an existing container and can affect the model-serving environment under test.

Mitigation: Use a dedicated test container and review the generated commands before execution.

## Reference(s):

- [Multi-Chip Error Classification](references/multichip-errors.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash snippets and a structured JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report includes status, per-run results, diff analysis, multi-chip component classification, and recommended_stack.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
