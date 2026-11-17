## Description:

Use fpx to capture an authenticated OurFamilyWizard browser session and curl to read or change messages, calendar events, expenses, journal entries, and attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to access their OurFamilyWizard data from shell scripts without running the ofw-mcp server. It includes examples for reading and writing messages, calendar events, expenses, journal entries, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented commands can create, change, or delete data in a shared family-court record, and the skill provides no dry-run or confirmation step for writes.

Mitigation: Before running a write or delete, review the method, target, and request body and confirm the intended change. Use read-only operations when changes are unnecessary, and re-fetch messages after sending or saving drafts to verify the result.

Risk: The captured bearer token provides authenticated access to the signed-in OurFamilyWizard account.

Mitigation: Keep the token private, avoid including it in logs or shared scripts, and recapture it only from the user's signed-in browser session when needed.

Risk: The security assessment reports a suspicious verdict with medium confidence and incomplete coverage.

Mitigation: Consider the reported write and delete capabilities before installing, especially when only data retrieval is needed; the scan is partial, so review the skill before relying on it.

## Reference(s):

- [OurFamilyWizard request examples](artifact/references/requests.md)
- [OurFamilyWizard API host](https://ofw.ourfamilywizard.com)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [fetchproxy extension notes](https://github.com/chrischall/fetchproxy#extension)
- [ClawHub skill page](https://clawhub.ai/chrischall/skills/ofw-fpx)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include read and write operations against a live account.]

## Skill Version(s):

2.29.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
