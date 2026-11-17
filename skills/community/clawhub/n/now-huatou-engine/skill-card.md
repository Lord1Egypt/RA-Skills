## Description:

Generate Zen-style huatou prompts by selecting or creating thought-provoking questions based on user context to aid mindfulness and self-inquiry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders can use this skill to produce concise Chinese-language Zen-style huatou prompts for mindfulness and self-inquiry across contexts such as anxiety, overthinking, decisions, emotions, and open reflection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future dynamic generation may send user situation text to a model route.

Mitigation: Review any implementation that adds qclaw/modelroute integration, including what user input is sent and how it is handled.

Risk: Meditation-style prompts may be inappropriate when a user expresses severe psychological crisis or self-harm intent.

Mitigation: Preserve and test the documented crisis-support behavior that avoids huatou generation and shows help information for crisis keywords.

Risk: The MVP references a static template data file that is not present in the submitted artifact.

Mitigation: Confirm the template file is supplied and reviewed before relying on static template selection behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perrykono-debug/skills/now-huatou-engine)
- [Source skill file](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Chinese-language prompt text, with markdown or JSON snippets only when describing generation behavior.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented MVP selects a static template, fills variables such as emotion and time wording, and returns one huatou prompt.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
