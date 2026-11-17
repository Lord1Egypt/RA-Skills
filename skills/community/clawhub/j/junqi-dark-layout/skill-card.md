## Description:

Generates Chinese Junqi dark-piece 25-cell layouts with LLM-authored strategy, strict Python validation, and optional image-card rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imcaptor](https://clawhub.ai/user/imcaptor)

### License/Terms of Use:

MIT-0

## Use Case:

External users and game-layout creators use this skill to ask an agent for Chinese Junqi dark-piece formations in a requested style, validate the 30-cell board against hard rules, and optionally render a visual layout card.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enforces opinionated Junqi strategy constraints and may reject layouts that some players would consider acceptable.

Mitigation: Treat the validator as the rule set for this release, explain constraint failures to the user, and regenerate only within those stated rules.

Risk: A generated board can be invalid if the validation step is skipped.

Mitigation: Run scripts/validate_layout.py before returning a final layout or rendering an image, and retry generation when validation reports errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imcaptor/skills/junqi-dark-layout)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [JSON layout object, concise Markdown guidance, shell commands for validation or rendering, and optional rendered image file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Layouts use a 30-item array with five fixed forbidden cells and 25 Junqi pieces; final layouts should pass local validation before being returned or rendered.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
