## Description: <br>
PRECC Token Saver instructs an agent to route shell commands through precc-hook so commands can be rewritten for directory fixes, output compression, and learned command heuristics before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yijunyu](https://clawhub.ai/user/yijunyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers using OpenClaw agents use this skill to reduce shell-command token usage and prevent repeated command failures by routing shell commands through PRECC before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes shell commands through external tooling that can rewrite commands before execution. <br>
Mitigation: Install only when PRECC is trusted for the target projects, review rewritten commands, and verify how to disable the hook. <br>
Risk: Setup guidance includes external installation and update flows that can change local tooling. <br>
Mitigation: Prefer pinned or package-manager installs, review update behavior, and avoid curl-to-bash installation in sensitive environments. <br>
Risk: Optional session-history ingestion can expose sensitive local workflow data. <br>
Mitigation: Avoid broad history ingestion on sensitive work and confirm how learned local data can be cleared. <br>


## Reference(s): <br>
- [PRECC project homepage](https://github.com/yijunyu/precc-cc) <br>
- [OpenClaw native PreToolUse hook issue](https://github.com/openclaw/openclaw/issues/7597) <br>
- [ClawHub skill page](https://clawhub.ai/yijunyu/precc-token-saver) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with JSON hook payload examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides the agent to invoke precc-hook before shell execution and may result in rewritten shell commands; hook errors fall back to the original command.] <br>

## Skill Version(s): <br>
0.1.8 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
