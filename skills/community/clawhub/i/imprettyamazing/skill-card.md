## Description:

Interact with I'm Pretty Amazing (imprettyamazing.com) -- a platform for tracking and celebrating accomplishments, including posting wins, tracking achievements, managing profiles, commenting on or liking wins, following users, submitting feedback, and suggesting wins after notable accomplishments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macksmind](https://clawhub.ai/user/macksmind)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to interact with the I'm Pretty Amazing service for accomplishment tracking, profile management, social actions, and feedback submission. The skill guides authenticated API use and requires confirmation before account creation or other state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable account session tokens may be stored in plaintext in TOOLS.md, which could expose the account if that file is accessible to other users, extensions, backups, or future agent sessions.

Mitigation: Prefer session-only login for sensitive accounts; persist tokens only after explicit user opt-in, protect TOOLS.md, and clear or revoke saved tokens if exposure is suspected.

Risk: The skill handles login credentials and authenticated cookie tokens for a third-party service.

Mitigation: Send credentials only to the documented API login endpoint, never store email or password, and avoid printing full session-token values in chat or logs.

Risk: State-changing actions can create accounts, post wins, update profiles, submit feedback, or modify social relationships.

Mitigation: Require explicit user confirmation before POST, PATCH, or DELETE requests, including account creation.

## Reference(s):

- [I'm Pretty Amazing API Reference](references/api.md)
- [I'm Pretty Amazing](https://imprettyamazing.com)
- [I'm Pretty Amazing API](https://api.imprettyamazing.com)
- [ClawHub Skill Page](https://clawhub.ai/macksmind/skills/imprettyamazing)
- [ClawHub Publisher Profile](https://clawhub.ai/user/macksmind)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with curl commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local session-token configuration only with user opt-in.]

## Skill Version(s):

0.2.4 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
