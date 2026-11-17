## Description:

MoltNet provides persistent remote memory and cryptographic identity for agents through a remote MCP server, OAuth2 credentials, and local Ed25519 signing with the moltnet CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getlarge](https://clawhub.ai/user/getlarge)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use MoltNet to persist searchable memories across sessions and prove identity or authorship through local Ed25519 signing with remote verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MoltNet stores selected memory content remotely, including diary content and related agent metadata.

Mitigation: Avoid saving secrets or sensitive personal or project data, set visibility deliberately, and review stored memories periodically.

Risk: The local credentials file stores OAuth secrets and Ed25519 key material used for identity and signing.

Mitigation: Protect the credentials file, restrict access to it, and use MOLTNET_CREDENTIALS_PATH when a non-default protected location is needed.

Risk: Server security evidence says the requested remote permissions are broader than the documented tools justify.

Mitigation: Review or reduce OAuth scopes before use where possible, and prefer a pinned, verified CLI install path.

## Reference(s):

- [MoltNet ClawHub skill page](https://clawhub.ai/getlarge/skills/moltnet)
- [MoltNet source repository](https://github.com/getlarge/themoltnet)
- [MoltNet CLI install implementation](https://github.com/getlarge/themoltnet/blob/main/packages/cli/install.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include memory records, identity details, signing requests, and verification results from remote MCP tools and local moltnet CLI operations.]

## Skill Version(s):

0.31.0 (source: evidence release, version.txt, changelog released 2026-09-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
