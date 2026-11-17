## Description:

Onboard a merchant into the Auto Google Review Reply product: register/login, connect a Google Business Profile, benefit from a 5-day free trial (membership check, no forced payment), and configure AI auto-reply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheaplightstore](https://clawhub.ai/user/cheaplightstore)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants use this skill to set up Auto Google Review Reply by signing in, connecting an existing Google Business Profile, checking trial or membership status, and enabling AI-generated review replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived bearer tokens may be exposed through URLs or persistent storage.

Mitigation: Use a trusted backend, avoid bearer tokens in URLs, prefer short-lived one-time handoff codes, store secrets only in the designated environment location, and mask tokens in diagnostics.

Risk: The skill can make real account, Google Business linking, auto-reply configuration, and checkout-initiation changes.

Mitigation: Require clear merchant confirmation before linking accounts, changing auto-reply settings, or starting payment, and verify membership status before checkout.

Risk: OAuth or handoff redirects could send sensitive authorization material to an unintended destination.

Mitigation: Restrict redirects to allowlisted HTTPS destinations and validate return URLs before issuing handoff or OAuth links.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cheaplightstore/skills/google-autoreply-setup)
- [Auto Google Review Reply API Base](https://apprest.mytruststores.com/adminServer)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance with structured API request and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform account setup, Google Business linking, membership checks, auto-reply configuration, and checkout initiation when authorized by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
