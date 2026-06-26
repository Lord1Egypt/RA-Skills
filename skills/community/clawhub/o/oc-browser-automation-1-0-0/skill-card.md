## Description: <br>
Browser control guidance that wraps OpenClaw browser operations for web automation, screenshots, page snapshots, clicking, typing, tab management, file upload, download, and debugging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlvwlw](https://clawhub.ai/user/vlvwlw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation-focused agents use this skill to control a browser for page navigation, screenshots, DOM snapshots, element interaction, form filling, downloads, uploads, and browser debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over a real browser session, including logged-in pages. <br>
Mitigation: Use the default or a separate sandbox browser profile, and avoid personal Chrome profiles unless logged-in access is required. <br>
Risk: Browser actions can submit forms, change account state, upload files, download sensitive content, or inspect network requests. <br>
Mitigation: Require explicit confirmation before state-changing actions, file transfers, sensitive downloads, request inspection, or interactions with account settings. <br>
Risk: Screenshots, snapshots, console output, traces, and network summaries may expose private data from pages the browser can access. <br>
Mitigation: Review captured browser output before sharing it and avoid capturing logged-in or sensitive pages unless necessary for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlvwlw/oc-browser-automation-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline browser command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser-tool use may produce screenshots, page snapshots, console output, network request summaries, traces, uploads, and downloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
