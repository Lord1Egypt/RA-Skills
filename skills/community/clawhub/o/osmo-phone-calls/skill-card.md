## Description:

Make and manage real phone calls through OsmO, then return call outcomes, summaries, and transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getosmo](https://clawhub.ai/user/getosmo)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an AI assistant to place or manage calls to businesses or contacts, with the recipient and call script confirmed before dialing. The assistant can report call results and provide available summaries, transcripts, and recording links.

### Deployment Geography for Use:

United States, Canada, United Kingdom, and Australia (free-credit availability stated; broader availability is not specified).

## Known Risks and Mitigations:

Risk: The security review was partial and does not guarantee that every artifact behavior was inspected.

Mitigation: Review the skill before connecting to OsmO, and treat the benign verdict as limited to the scan described in the release evidence.

Risk: A placed call reaches a real person and may convey information on the user's behalf.

Mitigation: Show the recipient and exact words first, place the call only after the user's explicit confirmation, and do not provide sensitive credentials or identity details.

Risk: Connecting requires phone-based sign-in to OsmO.

Mitigation: Have the user complete sign-in in the browser; never request, store, or repeat their one-time code in chat.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/getosmo/skills/osmo-phone-calls)
- [OsmO](https://getosmo.app)
- [OsmO MCP server](https://api.getosmo.app/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language call updates and summaries, with available transcripts, recording links, and Markdown setup instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls are placed only after the user confirms the recipient and exact call script; returned call details depend on OsmO's results.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
