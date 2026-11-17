## Description:

Nella provides codebase-aware search and indexing for non-trivial repositories, enabling symbol location, call tracing, dependency checks, and persistent session context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pablomanjarres](https://clawhub.ai/user/pablomanjarres)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use Nella to index repositories, search code semantically or lexically, trace relationships, preserve session context, and check assumptions or dependency drift during codebase work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository indexing can expose sensitive code to external embedding services or hosted infrastructure.

Mitigation: Decide whether the target repository may be indexed before use; for sensitive code, use a reviewed, version-pinned local install and review .nellaignore exclusions before indexing.

Risk: Credentials and telemetry may persist outside the repository.

Mitigation: Disable telemetry if undesired and protect or remove ~/.nella/auth.json when not in use.

Risk: Client setup can install mutable MCP configuration used by coding agents.

Mitigation: Review generated client configuration before deployment and pin the package version where repeatability matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pablomanjarres/skills/nella)
- [Hosted Nella MCP endpoint](https://mcp.getnella.dev/mcp)
- [README](README.md)
- [Nella Skill Definition](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, text responses, JSON MCP payloads, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return indexed search results, session context, assumption status, and dependency drift summaries.]

## Skill Version(s):

0.2.7 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
