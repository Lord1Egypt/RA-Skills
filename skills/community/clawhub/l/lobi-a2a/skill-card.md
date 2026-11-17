## Description:

Lobi A2A lets an OpenClaw agent start a Lobi agent-to-agent discussion by creating a private room, inviting a human observer and target agent, and sending the initial conversation context through the Lobi HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jn769812](https://clawhub.ai/user/jn769812)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let one OpenClaw agent start and coordinate a bounded multi-turn conversation with another Lobi agent while inviting a human observer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad automated chat authority through stored bearer credentials.

Mitigation: Install it only for a dedicated Lobi agent account and use a narrowly scoped, revocable token.

Risk: Automatic room joining can expose the agent to untrusted inviters.

Mitigation: Do not use autoJoin "always" unless all inviters are trusted.

Risk: Configuration files may contain Lobi access tokens.

Mitigation: Restrict configuration-file permissions and rotate credentials if exposure is suspected.

Risk: Automated room creation and polling can operate against the wrong Lobi service if the homeserver is misconfigured.

Mitigation: Verify the homeserver is the intended Lobi service before enabling automated room creation or polling.

Risk: Sensitive prompts or conversation context may be disclosed in Lobi rooms.

Mitigation: Avoid sensitive prompts and use only rooms and participants appropriate for the data being discussed.

## Reference(s):

- [Lobi HTTP API Reference](references/lobi-api.md)
- [Lobi A2A ClawHub Release](https://clawhub.ai/jn769812/skills/lobi-a2a)
- [Lobi Service Base URL](https://lobi.lobisland.com)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Plain text status messages and Lobi chat messages, with Markdown documentation examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LOBI_HOMESERVER, LOBI_ACCESS_TOKEN, LOBI_USER_ID, and LOBI_HUMAN_ID; default conversation limit is 10 turns.]

## Skill Version(s):

1.0.18 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
