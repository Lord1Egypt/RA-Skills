## Description:

Scan AI-generated code for hallucinated packages, stale APIs, security anti-patterns, and over-engineering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raye-deng](https://clawhub.ai/user/raye-deng)

### License/Terms of Use:

BSL 1.1

## Use Case:

Developers and engineering teams use this skill to scan pull requests, CI/CD changes, and third-party AI-generated code for defects that ordinary linters may miss.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable, unpinned third-party execution in npm, GitHub Action, and MCP setup paths can change behavior between reviews.

Mitigation: Pin npm package versions, use lockfile-backed installs in CI, pin the GitHub Action to a commit SHA, and pin or review the MCP server version before use.

Risk: Repository scanning may expose source code, secrets, or tokens to tools with broader access than needed.

Mitigation: Run scans with the minimum repository, token, secret, and network permissions required for the selected scan level.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raye-deng/skills/open-code-review)
- [Project homepage](https://github.com/raye-deng/open-code-review)
- [Open Code Review portal](https://codes.evallab.ai)
- [MCP server endpoint](https://open-code-review-mcp.v2ray-seins.workers.dev/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown with shell commands, YAML and JSON configuration snippets, and scanner output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SARIF files when the scanner is configured with SARIF output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
