## Description:

Upload files to lmfiles.com and return public download links via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[setdemos](https://clawhub.ai/user/setdemos)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to register lmfiles.com accounts, upload files, retrieve public download links, inspect file metadata, list account files, and delete uploaded files through CLI-style API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files are publicly downloadable by anyone with the URL.

Mitigation: Confirm each file is safe to publish and avoid uploading secrets, credentials, or private data.

Risk: The skill uses LMFILES_API_KEY and LMFILES_BOOTSTRAP_TOKEN credentials.

Mitigation: Keep credentials out of command lines and logs, and rotate the bootstrap token if exposed.

Risk: The delete helper removes files by ID without an interactive confirmation.

Mitigation: Double-check file IDs before deletion.

## Reference(s):

- [LMFiles service docs](https://lmfiles.com/docs)
- [LMFiles OpenAPI schema](https://lmfiles.com/openapi.json)
- [LMFiles API host](https://lmfiles.com)
- [ClawHub skill page](https://clawhub.ai/setdemos/skills/lmfiles)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce public file URLs, file IDs, account metadata, and deletion/listing command results from lmfiles.com API calls.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
