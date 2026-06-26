## Description: <br>
Generate a full Phoenix JSON API from an OpenAPI spec or natural language description. Creates contexts, Ecto schemas, migrations, controllers, JSON views/renderers, router entries, ExUnit tests with factories, auth plugs, and tenant scoping. Use when building a new Phoenix REST API, adding CRUD endpoints, scaffolding resources, or converting an OpenAPI YAML into a Phoenix project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gchapim](https://clawhub.ai/user/gchapim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to generate or extend Phoenix JSON APIs from OpenAPI specifications or natural language descriptions, including schemas, migrations, contexts, controllers, router entries, authentication plugs, tenant scoping, and tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tenant-security examples can teach applications to expose one tenant's data to another. <br>
Mitigation: Review and harden generated authorization code; derive tenant identity from authenticated claims or verified membership, scope every read, update, and delete by tenant, and add cross-tenant denial tests before using generated APIs. <br>


## Reference(s): <br>
- [Phoenix conventions reference](artifact/references/phoenix-conventions.md) <br>
- [Ecto patterns reference](artifact/references/ecto-patterns.md) <br>
- [Test patterns reference](artifact/references/test-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/gchapim/phoenix-api-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Phoenix and Elixir code, file plans, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or generate Phoenix project files such as migrations, Ecto schemas, contexts, controllers, JSON renderers, router entries, plugs, tests, and factories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
