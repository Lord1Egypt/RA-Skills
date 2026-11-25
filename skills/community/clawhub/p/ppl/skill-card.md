## Description:

Create and manage AI series and videos on PPL (ppl.xyz) for a creator through the PPL connector: read their characters, series and world, write a prompt for a video model, quote the gem price, render an episode as a draft, follow the job, manage series, world assets, collabs and drafts, and read stats and earnings. Use when the user mentions PPL, their PPL characters or series, making or editing an episode, a collab, gems, or their PPL drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pplxyz](https://clawhub.ai/user/pplxyz)

### License/Terms of Use:

MIT-0

## Use Case:

External creators use this skill to manage their PPL characters, series, video drafts, and related account activity through an authorized PPL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may invoke PPL actions when a user only mentions the service in passing.

Mitigation: Confirm the user intends PPL account work before making changes or starting a render.

Risk: The connection uses OAuth to access the creator's PPL account and can spend gems on creation or editing actions.

Mitigation: Review the requested access and daily gem limit during sign-in; check the current quote and get clear approval before any action that spends gems.

## Reference(s):

- [PPL MCP](https://www.ppl.xyz/mcp)
- [PPL tool reference](artifact/references/tools.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Video drafts, Image drafts]

**Output Format:** [Natural language guidance and prompts, plus PPL video and image drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is saved as drafts; publishing requires a separate user-directed action.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
