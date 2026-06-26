## Description: <br>
Exports Markdown notes to Smartisan-style long PNG images through a configurable notes-export-api endpoint, optionally uploading referenced local images first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoolee](https://clawhub.ai/user/zhaoolee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and note-taking users use this skill to export inline Markdown or local Markdown files as Smartisan-style PNG note images. It is useful for batch note image generation, including Markdown files that reference local images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown note content may be sent to a remote export service when no trusted local endpoint is configured. <br>
Mitigation: Use an explicit local or trusted endpoint through --endpoint or NOTES_EXPORT_API_BASE_URL before exporting sensitive notes. <br>
Risk: Local images referenced by Markdown files can be uploaded to the same export service during export. <br>
Mitigation: Review Markdown image references before export and avoid private local images unless the configured service is trusted. <br>
Risk: Local .env files are sourced during execution and can change the export endpoint. <br>
Mitigation: Inspect repository and skill .env files before running the script and set the intended endpoint explicitly. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zhaoolee/notes-export-api) <br>
- [notes-export-api project link from skill artifact](https://github.com/zhaoolee/notes) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; script output is a PNG file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports inline Markdown or a UTF-8 Markdown file, optional filename, optional theme, and endpoint configuration through command arguments or NOTES_EXPORT_API_BASE_URL.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
