## Description: <br>
A local web-based Markdown editor that starts a Flask server for live preview, synchronized scrolling, toolbar-assisted editing, and saving Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyunnet](https://clawhub.ai/user/xiyunnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and documentation maintainers use this skill to open a local Markdown editing interface, preview formatted output, and save changes to selected Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: While running, the local browser-accessible server can read and write local files with limited protection. <br>
Mitigation: Run it only on trusted files, keep it bound to localhost, and restrict use to an approved workspace or explicit file selections. <br>
Risk: Broad browser access controls can expose file operations to unwanted local web requests. <br>
Mitigation: Disable broad CORS and add a per-session token or CSRF protection before using it with sensitive content. <br>
Risk: Automatic shutdown from page hide or unload events can stop the editor unexpectedly. <br>
Mitigation: Save work before closing the browser tab and consider removing automatic shutdown behavior in managed environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiyunnet/local-markdown-editor) <br>
- [Markdown Guide](https://www.markdownguide.org/) <br>
- [Flask Documentation](https://flask.palletsprojects.com/) <br>
- [Showdown.js](https://github.com/showdownjs/showdown) <br>
- [CodeMirror](https://codemirror.net/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files edited through a local web interface with setup and usage commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Flask server and writes changes back to selected Markdown files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
