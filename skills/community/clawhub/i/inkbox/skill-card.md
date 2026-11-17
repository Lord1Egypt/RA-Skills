## Description:

Send and receive emails and phone calls via Inkbox agent identities, including inbox search, thread review, outbound messages and calls, call transcripts, vault credentials, and identity setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inkbox](https://clawhub.ai/user/inkbox)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw agent operate Inkbox identities for email, phone, transcript, and encrypted credential workflows. It is intended for agents that need explicit user-confirmed communication actions and scoped access to Inkbox resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inkbox API keys and vault secrets can be exposed if stored or printed carelessly.

Mitigation: Use a scoped API key, store it through the strongest OpenClaw secret mechanism available, avoid printing decrypted vault payloads, and rotate any key or secret that may have been exposed.

Risk: The skill depends on mutable third-party code through the @inkbox/sdk dependency path.

Mitigation: Install only when the Inkbox publisher and SDK dependency path are trusted, and prefer isolated or disposable Node environments for SDK use unless the user explicitly requests workspace installation.

Risk: Outbound email and phone actions can contact external recipients or numbers.

Mitigation: Confirm recipients, subjects, message bodies, and phone numbers with the user before sending email or placing calls.

Risk: Unlocked vault state can make decrypted credentials available to agent workflows.

Mitigation: Unlock the vault only for the needed task, rely on identity-scoped access rules where possible, and refresh or end the session when credential access is no longer required.

## Reference(s):

- [Inkbox homepage](https://inkbox.ai)
- [Inkbox console](https://console.inkbox.ai)
- [OpenClaw](https://openclaw.ai)
- [ClawHub Inkbox skill page](https://clawhub.ai/inkbox/skills/inkbox)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed SDK calls, setup commands, configuration snippets, message summaries, call transcript summaries, and credential-handling guidance.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
