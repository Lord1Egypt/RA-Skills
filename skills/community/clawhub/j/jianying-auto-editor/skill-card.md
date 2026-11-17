## Description:

Automate Jianying draft generation from local media plus a cloud editing API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video workflow operators use this skill to scan a local media folder, request editing decisions from a configured cloud API, and generate Jianying-oriented draft JSON files for short-form video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured cloud service receives filenames, paths, media metadata, task settings, and execution reports.

Mitigation: Use a minimal task-specific material_path, send only media intended for the task, and treat the selected API service as trusted for that metadata.

Risk: The example configuration uses a default HTTP API endpoint and the skill sends the API key in an Authorization header.

Mitigation: Replace the example endpoint with a trusted HTTPS API before using a real key, and avoid committing populated config files.

Risk: The skill writes output files to jianying_draft_path and may create a task-specific subdirectory from the returned task ID.

Mitigation: Configure a dedicated writable output directory and validate cloud task IDs before routine use.

Risk: Running through npx can fetch the package dynamically.

Mitigation: Pin the package version and review the installed artifact before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afengzi/skills/jianying-auto-editor)
- [ClawHub publisher profile](https://clawhub.ai/user/afengzi)
- [ClawHub metadata homepage](https://github.com/imfengziaaa/video-auto-editor-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples; runtime output is JSON files and a JSON execution summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft-meta.json, draft-content.json, and execution-report.json in the configured Jianying draft directory.]

## Skill Version(s):

0.1.1 (source: server release metadata, manifest.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
