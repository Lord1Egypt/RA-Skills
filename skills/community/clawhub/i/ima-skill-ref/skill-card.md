## Description:

Unified IMA OpenAPI skill for managing notes and knowledge bases, including search, browsing, file upload, URL import, note creation, and append workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dayofyear](https://clawhub.ai/user/dayofyear)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to operate an authorized IMA account through repeatable note and knowledge-base workflows. It helps agents search, read, create, append, upload, and import content while following documented IMA API parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generic Node API helper can send IMA API credentials to arbitrary URLs when an untrusted absolute path is supplied.

Mitigation: Prefer the module-specific helpers or allow only relative IMA OpenAPI paths under ima.qq.com before running the generic helper.

Risk: The file-upload workflow handles temporary COS credentials and may expose them through command-line arguments, logs, or predictable temporary files.

Mitigation: Use the skill only in a trusted environment, prefer environment variables for long-lived IMA credentials, avoid logging COS secrets, clean temporary credential files, and rotate credentials after any untrusted run.

Risk: Append and knowledge-base add workflows can modify user notes or knowledge-base contents.

Mitigation: Confirm the target note, knowledge base, folder, and duplicate-name handling before executing write or upload commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dayofyear/skills/ima-skill-ref)
- [IMA homepage](https://ima.qq.com)
- [IMA OpenAPI credential page](https://ima.qq.com/agent-interface)
- [IMA notes API reference](notes/references/api.md)
- [IMA knowledge-base API reference](knowledge-base/references/api.md)
- [Permission and credential notes](PERMISSIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and optional JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY environment variables or ~/.config/ima credential files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
