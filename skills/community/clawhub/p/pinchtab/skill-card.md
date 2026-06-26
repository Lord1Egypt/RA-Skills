## Description: <br>
Use this skill when a task needs browser automation through PinchTab: open a website, inspect interactive elements, click through flows, fill out forms, scrape page text, reuse a dedicated automation profile with user approval, export screenshots or PDFs, manage multiple browser instances, or fall back to the HTTP API when the CLI is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinchtab](https://clawhub.ai/user/pinchtab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use PinchTab to drive local browser sessions for navigation, page inspection, form interaction, data extraction, screenshots, PDFs, and HTTP API based automation. It is useful when browser work should be token-efficient and grounded in fresh accessibility references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can operate in authenticated sessions and may perform sensitive account, payment, or data-changing actions. <br>
Mitigation: Use a dedicated low-privilege browser profile and require user confirmation before account changes, payments, deletions, permission changes, or other critical actions. <br>
Risk: Eval, cookie access, network export, downloads, uploads, and guards-down behavior can expose private data or broaden the agent's authority. <br>
Mitigation: Keep these controls disabled unless the current task requires them, use the narrowest configuration possible, and redact or delete sensitive exports after use. <br>
Risk: Challenge solving, stealth, and fingerprint features can create authorization and policy risk on third-party sites. <br>
Mitigation: Use these features only with explicit authorization for the current site and task, and leave them disabled for normal browsing automation. <br>


## Reference(s): <br>
- [PinchTab GitHub repository](https://github.com/pinchtab/pinchtab) <br>
- [Full API](references/api.md) <br>
- [Minimal env vars](references/env.md) <br>
- [Agent optimization](references/agent-optimization.md) <br>
- [Profiles](references/profiles.md) <br>
- [MCP](references/mcp.md) <br>
- [Security model](TRUST.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser observations may include compact accessibility snapshots, text extracts, diffs, screenshots, PDFs, network exports, and API responses depending on the selected PinchTab command.] <br>

## Skill Version(s): <br>
0.13.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
