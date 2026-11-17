## Description:

Browse, search, and analyze Chia NFTs, collections, marketplace activity, and profiles through the public MintGarden API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to query Chia NFT collections, individual NFTs, trading activity, marketplace statistics, and public profiles from MintGarden in CLI, messaging, or agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, wallet or profile identifiers, NFT IDs, and collection IDs are sent to the public MintGarden API.

Mitigation: Avoid submitting sensitive or private identifiers unless the user is comfortable exposing those lookups to a public third-party API.

Risk: The release depends on HTTP client dependencies that may need updates for production or shared environments.

Mitigation: Update and re-lock dependencies before deployment, then rerun dependency and security checks.

## Reference(s):

- [ClawHub MintGarden Skill Page](https://clawhub.ai/koba42corp/skills/mintgarden)
- [MintGarden API Documentation](https://api.mintgarden.io/docs)
- [MintGarden Website](https://mintgarden.io)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Plain text responses with CLI and messaging-friendly formatting; JavaScript API client calls for integrations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the public MintGarden API without an API key; default query limits are 50 results and request timeout is 30 seconds.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
