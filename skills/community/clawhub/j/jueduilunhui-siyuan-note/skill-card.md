## Description:

This skill lets an agent read, search, create, append, clip, and sync content with a user-controlled SiYuan Note instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jueduilunhui](https://clawhub.ai/user/jueduilunhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent connect to SiYuan Note, search notebooks, create or append Markdown documents, clip articles, and save conversation records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary reports live-looking credentials and token-based access to SiYuan.

Mitigation: Rotate any exposed token if it was ever valid, store credentials in SIYUAN_API_TOKEN or a credential store, and avoid committing config-file tokens.

Risk: The skill can persist full conversations, clipped articles, and generated Markdown into a SiYuan workspace.

Mitigation: Require explicit user approval before writing, redact sensitive content before sync, and target only notebooks the user controls.

Risk: HTTP API access can expose note content or authorization tokens if used beyond a trusted local endpoint.

Mitigation: Restrict the SiYuan API to localhost or use HTTPS on trusted networks.

Risk: Included test and debug scripts can create or modify notes during execution.

Mitigation: Review script targets and configuration before running tests, and use a disposable notebook for validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jueduilunhui/skills/jueduilunhui-siyuan-note)
- [SiYuan Chrome extension reference](https://github.com/siyuan-note/siyuan-chrome)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, Python code snippets, shell commands, configuration examples, and SiYuan API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, a running SiYuan API endpoint, and SIYUAN_API_TOKEN or equivalent local configuration.]

## Skill Version(s):

2.0.0 (source: server release metadata, _meta.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
