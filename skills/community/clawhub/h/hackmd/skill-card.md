## Description:

Work with HackMD documents, including reading, creating, updating, deleting, and tracking changes for personal and team notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nulltea](https://clawhub.ai/user/nulltea)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to manage HackMD notes and team workspaces from the command line. It is also useful for checking whether tracked notes changed since the last review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide create, update, and delete operations on personal or team HackMD notes.

Mitigation: Require explicit confirmation before any create, update, or delete operation.

Risk: The tracking script can send the HackMD API token to the endpoint configured by HMD_API_ENDPOINT_URL.

Mitigation: Use a least-privileged HackMD token and leave HMD_API_ENDPOINT_URL unset unless using a trusted HackMD-compatible deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nulltea/skills/hackmd)
- [HackMD API endpoint](https://api.hackmd.io/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, note content, and optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires hackmd-cli, Node.js for change tracking, and HMD_API_ACCESS_TOKEN for authenticated HackMD access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
