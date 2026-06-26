## Description: <br>
Render markdown tables as PNG images for chat-friendly table sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirorab](https://clawhub.ai/user/kirorab) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Agents and developers use this skill when they need to turn markdown tables or simple markdown snippets into styled PNG files for chat or documentation output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided markdown table content is rendered in a browser without sanitization. <br>
Mitigation: Render only trusted markdown, or sanitize and escape user-controlled content before rendering. <br>
Risk: Browser rendering is launched with sandbox-disabling flags. <br>
Mitigation: Run rendering in an isolated environment and avoid disabling the browser sandbox unless the deployment environment clearly requires it. <br>
Risk: Rendered content may trigger browser-side network or script behavior if the implementation is broadened. <br>
Mitigation: Disable JavaScript or block external requests during rendering before broad use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirorab/md-table-image) <br>
- [Publisher Profile](https://clawhub.ai/user/kirorab) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files] <br>
**Output Format:** [PNG image file path and generated PNG image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports output path, optional title, viewport width, and dark theme options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
