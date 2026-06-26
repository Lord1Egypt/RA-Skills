## Description: <br>
Use when working with `.c4`/`.likec4` files or LikeC4 CLI/config questions where exact DSL/CLI syntax is required, especially for strict command/snippet-first answers, validate/export flags, predicates `*`/`_`/`**`, deployment snippets, dynamic views, or relationship extension matching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dc-ai-gh](https://clawhub.ai/user/dc-ai-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for precise LikeC4 DSL and CLI assistance, including architecture model snippets, validation/export commands, predicates, deployment views, dynamic views, and relationship matching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CLI commands can be incorrect for a local project or may affect an external LeanIX system when `sync --apply` is used. <br>
Mitigation: Review commands before execution, validate LikeC4 edits with `likec4 validate`, and provide LeanIX credentials or run `sync --apply` only when an update is intended. <br>


## Reference(s): <br>
- [LikeC4 Configuration Schema](https://likec4.dev/schemas/config.json) <br>
- [Bridge LeanIX Draw.io](references/bridge-leanix-drawio.md) <br>
- [CLI](references/cli.md) <br>
- [Configuration](references/configuration.md) <br>
- [Deployment](references/deployment.md) <br>
- [Dynamic Views](references/dynamic-views.md) <br>
- [Examples](references/examples.md) <br>
- [Identifier Validity](references/identifier-validity.md) <br>
- [Include Predicates and Wildcards](references/include-predicates-wildcards.md) <br>
- [Model](references/model.md) <br>
- [Predicates](references/predicates.md) <br>
- [Relationships Bidirectional](references/relationships-bidirectional.md) <br>
- [Specification](references/specification.md) <br>
- [Style Tokens and Colors](references/style-tokens-colors.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Views](references/views.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with LikeC4 snippets, CLI commands, and concise prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Snippet-first or command-first responses are expected when prompts request minimal, strict, or paste-ready output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
