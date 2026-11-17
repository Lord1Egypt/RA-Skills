## Description:

Provides a Rust, SeaORM, and frontend methodology for centralizing API contracts, constants, and database entities so agents can prevent implicit cross-boundary contract drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiamu-ssr](https://clawhub.ai/user/xiamu-ssr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when building Rust backends with SeaORM and any frontend to define API contracts, constants, and entities first, then check changes with bundled scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guidance is primarily in Chinese, which can lead to misunderstanding if the installer cannot read it accurately.

Mitigation: Translate and review the workflow before applying it to a production codebase.

Risk: gen_types.sh executes cargo test and overwrites the frontend type file path provided by the user.

Mitigation: Run it intentionally in a trusted project, pass an explicit output path, and review the working tree afterward.

Risk: check_contracts.sh uses shell-based static checks that can produce warnings requiring project-specific judgment.

Mitigation: Treat script findings as review inputs and confirm any flagged contract issue against the Rust and SeaORM code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiamu-ssr/skills/implicit-contract-defense)
- [check_contracts.sh](references/check_contracts.sh)
- [gen_types.sh](references/gen_types.sh)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Rust examples and bash script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local shell helpers for CI-style contract checks and ts-rs TypeScript generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
