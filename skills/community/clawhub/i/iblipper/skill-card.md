## Description: <br>
Generate kinetic typography animations for expressive agent-to-human communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyed](https://clawhub.ai/user/andyed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to create short animated typography links or GIF export URLs for greetings, announcements, celebrations, dramatic reveals, and other concise messages that benefit from visual emphasis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled URL helper can run local code if a specially crafted message is passed to scripts/iblipper.sh. <br>
Mitigation: Avoid running scripts/iblipper.sh on untrusted or copied message text until the encoder passes text as an argument or via stdin. <br>
Risk: Generated links send message text to an external GitHub Pages renderer. <br>
Mitigation: Do not place sensitive text in generated links, and verify any downloaded GIF before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyed/iblipper) <br>
- [iBlipper renderer](https://andyed.github.io/iblipper2025/) <br>
- [iBlipper Examples](references/examples.md) <br>
- [iBlipper Emotion Presets](references/emotions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Shareable URLs, Markdown links, GIF export URLs, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated links load an external GitHub Pages renderer; GIF export requires a browser download workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
