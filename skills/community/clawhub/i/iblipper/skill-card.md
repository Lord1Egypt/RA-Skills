## Description:

Generate kinetic typography animations for expressive agent-to-human communication. Use when you want to communicate with visual flair - animated text for announcements, alerts, greetings, dramatic reveals, or any message that deserves more than plain text. Outputs shareable URLs or can display in canvas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyed](https://clawhub.ai/user/andyed)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to turn short messages into iBlipper kinetic typography links or GIF export URLs for greetings, announcements, celebrations, dramatic reveals, and other expressive communications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can run unintended local code when given crafted message text.

Mitigation: Prefer direct link generation or run the helper only with trusted message text until its encoder passes the message as data.

Risk: Animated links can make important or urgent messages slower to understand.

Mitigation: Use plain text for urgent safety alerts and reserve animation for concise, non-critical communication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyed/skills/iblipper)
- [iBlipper web app](https://andyed.github.io/iblipper2025/)
- [iBlipper Examples](references/examples.md)
- [iBlipper Emotion Presets](references/emotions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown links, plain URLs, and concise workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [GIF export requires a browser session; generated links include message text in URL parameters.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
