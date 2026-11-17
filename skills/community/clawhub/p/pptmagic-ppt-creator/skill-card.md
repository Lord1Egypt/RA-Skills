## Description:

Use Banana Slides / pptmagic-compatible project APIs to create, continue, and export presentation decks from an idea, outline, or page-by-page description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin808](https://clawhub.ai/user/kevin808)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to drive a PPTMagic-compatible presentation service that creates, continues, and exports slide decks from a topic, outline, or detailed page descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deck prompts, outlines, slide descriptions, and uploaded template images may be sent to a public external PPTMagic deployment.

Mitigation: Avoid confidential, regulated, or sensitive material unless the user trusts the service operator; redact, summarize, or generalize sensitive source material before use.

Risk: Generated presentation content may use an unintended language when the user does not specify one.

Mitigation: Ask for or explicitly set the desired presentation language before generation when language matters.

## Reference(s):

- [API Workflow](references/api-workflow.md)
- [Curl Examples](references/curl-examples.md)
- [PPTMagic public deployment](https://openclaw-nopass.pptmagic.tech/)
- [ClawHub skill page](https://clawhub.ai/kevin808/skills/pptmagic-ppt-creator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status updates with project identifiers, page counts, task state, and export or download URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples and recovery guidance for failed generation or export steps]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
