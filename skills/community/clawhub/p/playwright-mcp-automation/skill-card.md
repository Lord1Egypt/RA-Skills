## Description: <br>
Launches and operates the Playwright MCP server so agents can browse live websites through structured browser automation tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanglinghao01-rakuten](https://clawhub.ai/user/zhanglinghao01-rakuten) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to Playwright MCP, automate authenticated browser workflows, collect screenshots or PDFs, and verify live web UI flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can control real browser sessions, including logged-in accounts and account-changing workflows. <br>
Mitigation: Require explicit confirmation before purchases, payments, posts, deletions, or other account-changing actions. <br>
Risk: Exposing the MCP server broadly can give unintended clients browser-control authority. <br>
Mitigation: Keep the server bound to localhost by default and avoid --allowed-hosts=* or 0.0.0.0 unless the service is isolated behind strong access controls. <br>
Risk: Persistent browser profiles and session artifacts can retain sensitive cookies, local storage, screenshots, PDFs, or logs. <br>
Mitigation: Use fresh per-task profiles, protect session artifacts, and delete sensitive browser state after the task is complete. <br>
Risk: Using the latest Playwright MCP package can change behavior across runs. <br>
Mitigation: Pin the Playwright MCP package version for repeatable automation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhanglinghao01-rakuten/playwright-mcp-automation) <br>
- [Playwright MCP upstream repository](https://github.com/microsoft/playwright-mcp) <br>
- [Playwright MCP Setup & Configuration](references/setup.md) <br>
- [Playwright MCP Tool Reference](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser snapshots, screenshots, PDFs, console logs, and network request evidence when the Playwright MCP server is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
