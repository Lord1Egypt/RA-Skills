## Description:

Access OurFamilyWizard messages, calendar, expenses, and journal from a shell using fpx to capture a signed-in browser session token and curl to call the service API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users who need to access OurFamilyWizard data from a shell or script can use the documented requests to read profiles, messages, calendar events, expenses, and journal entries, and to perform supported account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates this release suspicious with medium confidence because some account-changing actions are not disclosed by its stated data-access purpose; the scan was partial because referenced paths were unavailable.

Mitigation: Consider the suspicious verdict before installing. Review each command and avoid write or delete operations unless you trust the skill and accept that changes may be lasting and visible to the co-parent.

## Reference(s):

- [OurFamilyWizard requests reference](artifact/references/requests.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge source](https://github.com/nullnet-app/contextmint-bridge)
- [fetchproxy extension information](https://github.com/chrischall/fetchproxy#extension)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell code blocks and example API request and response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can read or modify the signed-in OurFamilyWizard account, depending on the operation used.]

## Skill Version(s):

2.30.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
