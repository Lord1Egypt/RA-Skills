## Description:

Helps an agent call the QAX Hunter OpenAPI to create, monitor, and download batch asset search exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biglizi775](https://clawhub.ai/user/biglizi775)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and developers use this skill to run Hunter asset-mapping searches, submit batch export jobs, poll task status, and retrieve exported results through a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote download response may choose a local filename and overwrite writable files.

Mitigation: Run from a low-risk working directory, set an explicit output path, and review or constrain download filename handling before deployment.

Risk: Hunter API keys may be exposed if passed directly on the command line or captured in logs.

Mitigation: Prefer HUNTER_API_KEY, use a limited-scope key where available, and avoid verbose HTTP or shell logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biglizi775/skills/hunterserach)
- [Hunter batch search OpenAPI endpoint](https://hunter.qianxin.com/openApi/search/batch)
- [Hunter batch download OpenAPI endpoint](https://hunter.qianxin.com/openApi/search/download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses HUNTER_API_KEY or an explicit API key, accepts Hunter query and export options, and may produce a downloaded export file path.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
