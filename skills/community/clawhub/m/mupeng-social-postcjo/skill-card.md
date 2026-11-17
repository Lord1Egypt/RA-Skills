## Description:

Create reviewed posts for Twitter and Farcaster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft, validate, preview, and publish social posts or replies for Twitter/X and Farcaster after explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent-assisted workflow can publish public posts or replies after approval.

Mitigation: Default to dry-run preview, show the exact final text and destinations, and publish only after explicit human approval of the unchanged payload.

Risk: Packaged backup material contains obsolete examples for plaintext credentials, wallet keys, and auto-confirm live posting.

Mitigation: Treat the backup file as obsolete, never use auto-confirm for live posts, and use protected secret management or tightly permissioned environment injection for credentials.

Risk: Malformed platform payloads, missing media, or wrong reply targets could publish unintended content.

Mitigation: Validate current platform limits, links, local media paths, attachment lists, and reply target URLs or IDs before requesting approval.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text preview with final post text, destinations, approval request, and resulting post URLs or IDs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run preview; live publishing requires explicit approval of the exact payload.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
