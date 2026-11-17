## Description:

Instant mock HTTP server from any OpenAPI 3.x or Swagger 2.0 spec that helps agents guide users through validating a spec, starting a local Stoplight Prism mock server, listing endpoints, and generating test curl commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, frontend teams, and API engineers use this skill to stand up a local mock API from an OpenAPI or Swagger specification for contract-first development, frontend unblockers, and integration testing without a live backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell command snippets may behave unexpectedly when used with untrusted spec paths or filenames.

Mitigation: Review generated commands before running them and use only trusted OpenAPI or Swagger spec files and filenames.

Risk: Unpinned downloaded tooling can change behavior between runs.

Mitigation: Prefer pinned Prism or Mockoon versions installed locally with a project lockfile instead of global or latest-version installs.

Risk: Mock servers can expose sensitive example data if bound broadly or populated with real tokens.

Mitigation: Keep the server bound to localhost and avoid real secrets, production tokens, or sensitive example data in served specs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-openapi-mock-server)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command snippets, endpoint summaries, troubleshooting notes, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local npm, npx, Docker, and curl commands for running and testing a mock server.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
