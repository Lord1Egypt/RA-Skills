## Description: <br>
Creates a pending HiJavis to-do card with a ready-to-paste Claude brainstorming prompt from recent voice or keyboard transcript context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuel-wei](https://clawhub.ai/user/samuel-wei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External HiJavis users and agent operators use this skill to turn recent brainstorm-worthy voice or keyboard transcript units into pending calendar to-do cards that hand off to Claude for an interactive brainstorming session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect recent voice or keyboard transcript units to identify brainstorm-worthy content. <br>
Mitigation: Install only when this transcript review behavior is desired, and review or discard unwanted pending cards in the HiJavis Calendar tab. <br>
Risk: Manual runs can scan the recent transcript window by default and may create a card from context the user did not intend to keep. <br>
Mitigation: Use the pending-card Confirm/Discard gate before saving cards to the calendar. <br>


## Reference(s): <br>
- [Brainstorming on ClawHub](https://clawhub.ai/samuel-wei/javis-brainstorming) <br>
- [HiJavis iPhone App](https://apps.apple.com/us/app/hijavis/id6745134765) <br>
- [to-do card contract](references/todo-card-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [JSON transcript fetch output and to-do-card payloads, Markdown chat digests, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces pending HiJavis calendar cards with ready-to-paste Claude prompts and source transcript references.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
