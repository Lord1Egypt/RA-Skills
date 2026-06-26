## Description: <br>
OctoFlow helps agents turn natural-language GPU compute, data analysis, image processing, machine learning, and code-generation requests into Vulkan-backed OctoFlow programs and commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikedconcepcion](https://clawhub.ai/user/mikedconcepcion) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical users use this skill to run GPU-accelerated data analysis, statistics, image processing, machine learning, and OctoFlow scripting workflows from an agent. It is also suitable for configuring the OctoFlow MCP server when an agent needs structured OctoFlow tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded binaries could be tampered with or mismatched for the release. <br>
Mitigation: Verify the downloaded OctoFlow binary against the published SHA-256 checksum before installing or running it. <br>
Risk: Granting broad file, network, or subprocess permissions can expose more local data or system capability than the task requires. <br>
Mitigation: Use the minimum necessary --allow-read, --allow-write, --allow-net, and --allow-exec scopes for each run. <br>
Risk: Local preference storage may retain frequently used modules or corrections between sessions. <br>
Mitigation: Run with --no-memory when local preference storage is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikedconcepcion/octoflow) <br>
- [OctoFlow documentation](https://octoflow-lang.github.io/octoflow/) <br>
- [OctoFlow GitHub repository](https://github.com/octoflow-lang/octoflow) <br>
- [OctoFlow v1.5.8 release downloads](https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/) <br>
- [OctoFlow releases](https://github.com/octoflow-lang/octoflow/releases) <br>
- [OctoFlow v1.5.8 checksums](https://github.com/octoflow-lang/octoflow/releases/download/v1.5.8/SHA256SUMS.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline code blocks, shell commands, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OctoFlow CLI commands, .flow code, MCP server configuration, and permission-scoped execution guidance.] <br>

## Skill Version(s): <br>
1.5.8 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
