## Description:

Onboards merchants into Auto Google Review Reply by helping them sign in, connect a Google Business Profile, confirm trial or membership status, and configure AI review auto-replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheaplightstore](https://clawhub.ai/user/cheaplightstore)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and their support operators use this skill to complete Auto Google Review Reply onboarding, including account access, Google Business Profile connection, free-trial or membership checks, and auto-reply configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived merchant session tokens and authentication handoffs.

Mitigation: Store authorization values only in the designated environment variable, avoid token-in-URL flows where possible, mask tokens in diagnostics, and reauthorize only after a 401 response.

Risk: The skill can connect or disconnect a Google Business Profile and enable automated public review replies.

Mitigation: Confirm the selected business location and auto-reply settings with the merchant before binding profiles or enabling reply automation.

Risk: The workflow may direct an expired merchant account to Stripe checkout.

Mitigation: Check membership status first and only initiate checkout after confirming that the free trial or paid membership has expired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cheaplightstore/skills/google-autoreply)
- [Auto Google Review Reply API Base](https://apprest.mytruststores.com/adminServer)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown guidance with backend API request details and configuration payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve authentication, Google Business Profile authorization, membership checks, auto-reply settings, and Stripe checkout handoff when a trial or membership has expired.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
