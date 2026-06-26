## Description: <br>
Advanced JSON editing for OpenClaw configuration files, tools, and data structures, including JSON5 configs, schema validation, merge patching, env var substitution, and type-safe modifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avirweb](https://clawhub.ai/user/avirweb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to edit, validate, patch, and troubleshoot OpenClaw JSON and JSON5 configuration safely, including provider, model, tool, channel, and environment-variable settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Config overwrite or patch commands could change working OpenClaw settings unexpectedly. <br>
Mitigation: Create backups before edits, review proposed patches, and run OpenClaw validation commands before relying on updated configuration. <br>
Risk: Configuration files and command output can contain API keys, tokens, or environment variable references. <br>
Mitigation: Prefer environment-variable substitution, avoid hardcoded secrets, restrict file permissions, and do not share outputs that may expose credentials. <br>
Risk: Provider and model guidance can become inaccurate if APIs, model names, or pricing change. <br>
Mitigation: Verify model IDs and provider details against the provider API before committing configuration changes. <br>


## Reference(s): <br>
- [OpenClaw JSON Editing Skill Page](https://clawhub.ai/avirweb/openclaw-json-editing) <br>
- [xAI Models API](https://api.x.ai/v1/models) <br>
- [OpenAI Models API](https://api.openai.com/v1/models) <br>
- [Together AI Models API](https://api.together.xyz/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, TypeScript, JSON, and JSON5 examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq for command-line JSON inspection examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
