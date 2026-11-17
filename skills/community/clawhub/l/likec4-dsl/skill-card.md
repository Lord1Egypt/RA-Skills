## Description:

Use when working with `.c4`/`.likec4` files or LikeC4 CLI/config questions where exact DSL/CLI syntax is required, especially for strict command/snippet-first answers, validate/export flags, predicates `*`/`_`/`**`, deployment snippets, dynamic views, or relationship extension matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dc-ai-gh](https://clawhub.ai/user/dc-ai-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to produce precise LikeC4 DSL snippets, validation commands, export commands, configuration guidance, and troubleshooting answers for architecture-as-code projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned LikeC4 CLI through a package runner can introduce supply-chain drift.

Mitigation: Prefer a local reviewed LikeC4 dependency or an exact pinned command such as `likec4@1.53.0`.

Risk: LeanIX sync with `--apply` can change LeanIX data when valid credentials are present.

Mitigation: Use LeanIX `--apply` only when intentionally changing LeanIX data with a valid token; otherwise prefer dry-run workflows.

## Reference(s):

- [Skill page](https://clawhub.ai/dc-ai-gh/skills/likec4-dsl)
- [CLI Reference](references/cli.md)
- [Project Configuration Reference](references/configuration.md)
- [Specification (LikeC4 DSL)](references/specification.md)
- [Model (LikeC4 DSL)](references/model.md)
- [Deployment (LikeC4 DSL)](references/deployment.md)
- [Views](references/views.md)
- [Dynamic Views](references/dynamic-views.md)
- [Predicates](references/predicates.md)
- [Include Predicates and Wildcards in Views](references/include-predicates-wildcards.md)
- [Identifier Validity](references/identifier-validity.md)
- [Style Tokens and Colors](references/style-tokens-colors.md)
- [Common Mistakes and Debugging](references/troubleshooting.md)
- [LeanIX Bridge and Draw.io Profile](references/bridge-leanix-drawio.md)
- [LikeC4 configuration schema](https://likec4.dev/schemas/config.json)
- [LikeC4 dynamic view documentation](https://likec4.dev/dsl/views/dynamic/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with LikeC4 and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact first-line commands or snippets when requested by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
