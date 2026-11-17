## Description:

Operate an already-open Hinge session in the browser or on iPhone to review profiles, triage the queue, analyze matches, draft respectful openers or replies, and execute explicit like, reply, or rose actions when the user has asked for autonomous sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdave211](https://clawhub.ai/user/jdave211)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to assist with live Hinge browsing, profile review, inbox triage, and respectful message drafting. It can also stage or perform likes, replies, and roses when the user has explicitly enabled autonomous sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in Hinge session and may send likes, skips, replies, or roses in daemon mode.

Mitigation: Use queue or read-only behavior until the user explicitly enables autonomous sending for the current session.

Risk: Dating screenshots, messages, observations, and preference files may be saved locally.

Mitigation: Disable screenshot retention where possible, keep notes minimal, and regularly delete hinge-data.

Risk: The skill may use OpenAI credentials while processing sensitive dating context.

Mitigation: Use a dedicated scoped API key and avoid sharing more profile or message context than the task requires.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdave211/skills/hinge-rizz-agent)
- [iOS Access](references/ios-access.md)
- [Rizz Style Notes](references/rizz-style-notes.md)
- [The Cut texting advice](https://www.thecut.com/article/how-to-text-flirt-examples-advice.html)
- [Lovepanky flirting examples](https://www.lovepanky.com/flirting-flings/naughty-affairs/flirty-text-examples)
- [wikiHow rizz examples](https://www.wikihow.com/Examples-of-Rizz-Lines)
- [wikiHow texting guidance](https://www.wikihow.com/How-to-Rizz-a-Girl-over-Text)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local queue, analysis, observation, and preference files during a live session.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
