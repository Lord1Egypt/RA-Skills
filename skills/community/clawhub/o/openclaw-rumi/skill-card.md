## Description:

Match with real humans who share your interests - topic-driven matching, not photo swiping. Chat through OpenClaw or on the web.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricky610329](https://clawhub.ai/user/ricky610329)

### License/Terms of Use:


## Use Case:

External OpenClaw users use Rumi to find real people for topic-driven conversations, including peer perspective, niche expertise, shared interests, and social discussion. The skill guides the agent through setup, matching, status checks, and optional chat relay after a match is found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Matching descriptions may include sensitive conversation context or private topics.

Mitigation: Share only details the user is comfortable sending to Rumi and avoid unnecessary personal, confidential, or regulated information.

Risk: The setup flow involves an API token that could be exposed if pasted into ordinary chat.

Mitigation: Use a secure secret-entry and storage mechanism when available, avoid pasting API tokens into normal chat, and rotate the token if it is exposed.

Risk: The skill connects users with real people, so safety expectations differ from AI-only chat.

Mitigation: Respect age-verification and minor-matching safeguards, do not share personal information beyond what the user chooses to reveal, and use the web chat option when appropriate.

## Reference(s):

- [Rumi ClawHub Skill Page](https://clawhub.ai/ricky610329/skills/openclaw-rumi)
- [ricky610329 Publisher Profile](https://clawhub.ai/user/ricky610329)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with tool-call instructions and user-facing chat text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce setup URLs, matching descriptions, status updates, icebreakers, chat links, and relayed chat messages.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
