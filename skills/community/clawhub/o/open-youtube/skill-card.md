## Description:

Open YouTube in the user's Brave browser and take the user to YouTube's homepage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to open the YouTube homepage in Brave while reusing an existing browser session and stopping before credential entry or account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may focus or open Brave and use an existing YouTube login state.

Mitigation: Run it only when browser focus and current session reuse are acceptable; the skill should stop at sign-in and avoid credential entry.

Risk: Browser automation could affect the user's YouTube account if the skill is extended beyond its documented scope.

Mitigation: Keep use limited to opening and verifying the YouTube homepage unless the user explicitly requests separate account actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-youtube)
- [YouTube homepage](https://www.youtube.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Concise status text with browser automation steps as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May focus or open Brave, reuse an existing YouTube tab, verify the destination, and stop if sign-in is required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
