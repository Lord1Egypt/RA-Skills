## Description: <br>
Multi-agent orchestration plugin for OpenCode that helps users install, configure, and operate oh-my-opencode features such as agent delegation, autonomous work modes, background tasks, category-based routing, model resolution, tmux integration, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[McOso](https://clawhub.ai/user/McOso) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to set up and operate oh-my-opencode as an OpenCode multi-agent harness for coding workflows, planning, delegated research, background execution, model routing, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables powerful autonomous and background coding workflows that can make or propose broad changes when run with permissive tool access. <br>
Mitigation: Run it deliberately in a clean branch or worktree, keep OpenCode permissions on ask or deny for risky commands, and review plans and diffs before relying on results. <br>
Risk: Parallel agents and premium model fallback chains can increase provider usage, cost, or rate-limit pressure. <br>
Mitigation: Monitor provider usage and cost, configure concurrency and model routing intentionally, and stop background or continuation workflows when finished. <br>
Risk: Installation and diagnostic workflows execute third-party package-manager commands and depend on OpenCode and upstream packages. <br>
Mitigation: Install only if you trust OpenCode, oh-my-opencode, and the upstream packages it runs; prefer package-manager installs over curl-to-bash where practical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/McOso/oh-my-opencode) <br>
- [Publisher profile](https://clawhub.ai/user/McOso) <br>
- [Project homepage](https://github.com/code-yeongyu/oh-my-opencode) <br>
- [Configuration Reference](references/configuration.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [OpenCode documentation](https://opencode.ai/docs/) <br>
- [oh-my-opencode schema](https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline commands, configuration examples, and workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest OpenCode, bunx, provider, tmux, and configuration commands for the user's environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
