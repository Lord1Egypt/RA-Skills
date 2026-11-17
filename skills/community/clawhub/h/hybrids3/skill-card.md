## Description:

Connect an agent to a self-hosted object store through its S3, HTTP, or MCP interface to manage objects and create presigned access links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Hybrids3 to upload, download, list, and manage objects in an existing self-hosted store. It can also create time-limited links for a specific object and connect storage tools over MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deletion confirmation weakness

Mitigation: Require explicit authorization for the exact bucket and key before deletion, and avoid bulk deletion.

Risk: Credential handling over HTTP and MCP

Mitigation: Use HTTPS for remote connections, limit credentials to the needed bucket, and keep keys and live presigned URLs out of shared prompts and logs.

Risk: Unpinned Docker images

Mitigation: Pin the container image to a reviewed version or digest before installation.

Risk: Incomplete scan coverage

Mitigation: Review the uninspected component and instruction text before installation; the scan covered 2 of 3 components.

## Reference(s):

- [Setup guide](references/setup.md)

## Skill Output:

**Output Type(s):** [API Calls, Files, Shell commands, Text]

**Output Format:** [S3, HTTP, or MCP requests and responses; shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transfers object data, returns object or bucket details and presigned links, and can delete or overwrite objects when requested. MCP downloads are limited to 50 MB.]

## Skill Version(s):

0.3.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
