## Description: <br>
Safe configuration file editing for JSON, YAML, TOML, and other config formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dougchambes](https://clawhub.ai/user/dougchambes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to safely read, edit, validate, merge, convert, and troubleshoot configuration files while preserving syntax and formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed configuration edits can break applications if syntax, schema, or runtime behavior is not validated. <br>
Mitigation: Back up files before destructive edits, review diffs, validate syntax with the appropriate parser or linter, and test changes in the application context before deployment. <br>
Risk: Configuration files such as .env files may contain secrets. <br>
Mitigation: Avoid exposing or committing secrets, use ignored local environment files for sensitive values, and inspect generated changes before sharing or publishing them. <br>


## Reference(s): <br>
- [Configuration Formats Reference](references/formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file changes; users should review diffs, keep backups, and validate configuration syntax before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
