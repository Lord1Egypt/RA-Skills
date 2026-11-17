## Description:

Open Reddit in the user's Brave browser and take the user to the Reddit homepage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to open Reddit in Brave, reuse an existing Reddit tab or session when available, and verify that the homepage loaded. The skill stops at sign-in prompts and does not handle credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may open Reddit in Brave using an already-signed-in browser session.

Mitigation: Install and invoke it only when using that existing Reddit session is acceptable; the skill stops at sign-in prompts and does not enter credentials.

Risk: Browser navigation could accidentally duplicate Reddit tabs or proceed before the destination is visible.

Mitigation: Reuse an existing Reddit tab when present, open only one destination tab otherwise, and verify that the Reddit homepage is visibly loaded before reporting success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-reddit)
- [Reddit homepage](https://www.reddit.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text guidance with browser navigation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May focus Brave, reuse an existing Reddit tab, or open one destination tab; stops at login prompts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
