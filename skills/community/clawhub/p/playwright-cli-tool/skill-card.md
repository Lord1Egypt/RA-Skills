## Description: <br>
Playwright CLI is a browser automation skill for controlling browsers, taking screenshots, filling forms, clicking elements, running code, managing sessions, intercepting network requests, and recording video or traces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chensu1234](https://clawhub.ai/user/chensu1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser testing, web interaction, data collection, screenshots, PDF export, network interception, and session workflows through Playwright CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad browser control, including stored data, uploads, page code execution, network capture, tracing, video, persistent state, and destructive session commands. <br>
Mitigation: Use a separate browser profile and test accounts, avoid sensitive logged-in sessions, and require explicit approval before run-code, uploads, cookie or storage changes, network capture, tracing, video, persistent state, delete-data, close-all, or kill-all. <br>
Risk: The npm package can affect local browser behavior and generated files if installed or run without verification. <br>
Mitigation: Pin and verify the npm package before installation and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chensu1234/playwright-cli-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and generated browser artifacts such as screenshots, PDFs, traces, videos, snapshots, cookies, and storage state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify browser session state, local files, cookies, localStorage, network routes, trace files, and video recordings depending on the invoked command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
