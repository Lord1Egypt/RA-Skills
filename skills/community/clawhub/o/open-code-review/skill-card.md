## Description: <br>
Scans AI-generated code for hallucinated packages, stale APIs, security anti-patterns, and over-engineering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raye-deng](https://clawhub.ai/user/raye-deng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan AI-generated code in pull requests, pre-merge quality gates, or third-party code reviews for AI-specific defects that traditional linters may miss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to third-party npm packages, a GitHub Action, and an MCP server. <br>
Mitigation: Verify package provenance, pin versions in CI, and review third-party code before installing or executing it. <br>
Risk: AI-powered scan levels may process private repository content through remote services when configured with API keys. <br>
Mitigation: Prefer local Ollama for private repositories and use scoped API keys when remote AI scans are enabled. <br>


## Reference(s): <br>
- [Open Code Review GitHub repository](https://github.com/raye-deng/open-code-review) <br>
- [Open Code Review portal](https://codes.evallab.ai) <br>
- [Open Code Review MCP endpoint](https://open-code-review-mcp.v2ray-seins.workers.dev/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/raye-deng/open-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code review findings] <br>
**Output Format:** [Markdown with inline bash, YAML, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide CLI scans, GitHub Action setup, SARIF output generation, and MCP server configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
