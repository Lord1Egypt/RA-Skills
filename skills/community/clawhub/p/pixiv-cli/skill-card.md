## Description:

Safely operate the pixiv-cli binary for Pixiv discovery, account actions, reverse image search, and downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flanchanxwo](https://clawhub.ai/user/flanchanxwo)

### License/Terms of Use:

MIT

## Use Case:

Agents use this skill to handle explicit Pixiv requests, including finding works and users, managing authorized account actions, and downloading selected content while protecting credentials and respecting user scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud vector search can send private or R18 thumbnails and query content to an external embedding service and may incur charges.

Mitigation: Use the local vector model when possible. Before cloud processing, review the provider's data handling and costs and explicitly authorize that scope.

Risk: Reverse image search uploads the selected image to third-party search providers.

Mitigation: Use only images the user is authorized to share and follow the providers' privacy boundaries.

## Reference(s):

- [Project homepage](https://github.com/FlanChanXwO/pixiv-cli)
- [Pixiv CLI reference](https://github.com/FlanChanXwO/pixiv-cli/blob/main/docs/en/cli-reference.md#drawing-tool-catalog)
- [MCP tool migration table](https://github.com/FlanChanXwO/pixiv-cli/blob/main/docs/en/mcp-tools.md#tool-migration)
- [Discovery and vector search guidance](artifact/references/discover.md)
- [Authentication and credential guidance](artifact/references/auth.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, NDJSON, Downloaded media files]

**Output Format:** [Concise text, structured CLI results, and requested media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results follow the requested scope; downloads write files to the selected destination.]

## Skill Version(s):

1.5.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
