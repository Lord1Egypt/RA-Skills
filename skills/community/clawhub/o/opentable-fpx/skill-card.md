## Description:

Query and manage OpenTable restaurant reservations from a shell with the fpx CLI through a signed-in browser tab, including searching, checking availability, listing reservations and favorites, and booking, modifying, or cancelling a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search OpenTable, inspect availability and account information, and manage restaurant reservations through shell commands when an OpenTable MCP server is not being used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking, modifying, or cancelling acts immediately on the signed-in account and may use a saved card.

Mitigation: Require explicit user approval before any write; review the booking details, selected seating, and cancellation policy first.

Risk: Temporary request files and logs may expose account data or security tokens.

Mitigation: Prefer in-memory request bodies or private temporary files with cleanup, and keep tokens out of logs.

Risk: The external fpx CLI and browser extension code have not been verified by the supplied security review.

Mitigation: Review or verify the CLI and extension before use, limit browser access to OpenTable, and revoke pairing when finished.

## Reference(s):

- [OpenTable FPX request catalogue](artifact/references/opentable-fpx-requests.md)
- [Initial state extraction helper](artifact/references/extract-initial-state.mjs)
- [OpenTable](https://www.opentable.com)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [Fetchproxy extension information](https://github.com/chrischall/fetchproxy#extension)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/opentable-fpx)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON data, Reservation guidance]

**Output Format:** [Markdown instructions with shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include commands for reading OpenTable data and managing reservations.]

## Skill Version(s):

1.4.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
