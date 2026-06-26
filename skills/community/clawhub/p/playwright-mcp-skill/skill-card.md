## Description: <br>
Run browser automation through @playwright/mcp over UXC stdio MCP, with daemon-friendly session reuse and safe action guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to navigate web pages, inspect DOM-oriented browser snapshots, and run scripted Playwright MCP browser actions from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent shared browser profiles can reuse logged-in sessions across accounts or trust boundaries. <br>
Mitigation: Prefer isolated mode by default and use shared profile commands only when session reuse is intentional. <br>
Risk: Stopping the UXC daemon may interrupt unrelated active UXC sessions. <br>
Mitigation: Use daemon stop only when switching shared-profile browser sessions and after checking that unrelated sessions do not need to remain active. <br>
Risk: Using the latest Playwright MCP package can change behavior over time. <br>
Mitigation: Pin the Playwright MCP package version when reproducible automation behavior is required. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON envelope fields for MCP command results.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
