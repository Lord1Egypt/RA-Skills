## Description:

Guides an OpenClaw agent through Space-only social matching: user onboarding, user-confirmed public profile drafting, immediate first recommendations, follow-up recommendation preferences, platform messages, and inbox polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikaqiu2333](https://clawhub.ai/user/pikaqiu2333)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to join a Space, confirm a public social profile, receive a first match recommendation, choose future recommendation and inbox-checking preferences, and send platform messages only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles social profiles and platform messages through a remote API.

Mitigation: Use it only with accounts, Spaces, and service operators the user trusts, and have the user review profile drafts and messages before submission.

Risk: Identity and session handling are weakly documented in the available evidence.

Mitigation: Review the connection and authorization flow before installation and avoid using operator credentials in the normal user workflow.

Risk: Remote user-generated Markdown is treated as Space context for recommendations.

Mitigation: Treat remote Space context as untrusted input and require user confirmation before writing profiles, reporting recommendations, or sending messages.

Risk: Reminder and polling preferences may cause the agent to act on stored user preferences over time.

Mitigation: Ask the user to choose reminder behavior explicitly and state when automatic checks are not available in the runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pikaqiu2333/skills/perfectmatch)
- [Skill homepage](https://pikaqiu2333.github.io/social-radar-skill/)
- [Social Radar API base](https://api.clawspace.top)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Configuration]

**Output Format:** [Conversational guidance with JSON and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-visible profile drafts, recommendation explanations, message prompts, preference handling guidance, and API request shapes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
