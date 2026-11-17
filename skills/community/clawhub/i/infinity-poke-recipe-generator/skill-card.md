## Description:

Generate a small, specific, daily-life Poke recipe MVP from idea to Kitchen-ready draft, including recipe fields, integrations, sandbox tests, publish-readiness checks, and an improvement loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skylinehk](https://clawhub.ai/user/skylinehk)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Poke recipe creators use this skill to scaffold narrow, daily-life Poke recipe MVPs and prepare Kitchen-ready recipe, integration, sandbox, verdict, README, and upload-instruction materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Kitchen instructions can include copyable shell commands derived from recipe data.

Mitigation: Review generated commands before execution and verify integration URLs and names are plain data without shell syntax.

Risk: The skill suggests mutable npx poke@latest commands.

Mitigation: Pin the Poke CLI version before running bootstrap commands.

Risk: Integration endpoints may be placeholders or may need MCP endpoint selection.

Mitigation: Replace TODO endpoints, verify authentication requirements, and test the integration connection before publishing.

## Reference(s):

- [Recipe Template](artifact/references/recipe-template.json)
- [Integration Template](artifact/references/integration-template.json)
- [Verdict Checklist](artifact/references/verdict-checklist.md)
- [Poke Recipes](https://poke.com/recipes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus JSON templates and generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include copyable CLI bootstrap commands and generated recipe folders under recipes/poke/<slug>/.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
