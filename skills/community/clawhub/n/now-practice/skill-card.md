## Description:

Now Practice provides a Chinese-language 60-second mindfulness practice flow with fixed stop, breathing, huatou, and return steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to guide short Chinese-language mindfulness sessions for anxiety, overthinking, decision stress, emotional intensity, or free practice. Agents and app builders can use it to generate the fixed four-step flow, choose scene-specific huatou prompts, and describe local completion tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Practice history may persist locally in browser storage when a frontend implements the disclosed completion tracking behavior.

Mitigation: Disclose local storage use and provide users with browser site-data clearing or an app-level history reset path.

Risk: The practice flow is written for Chinese-language use, so untranslated prompts may be misunderstood by other users.

Mitigation: Use the Chinese prompts as authored or provide reviewed translations before deployment to non-Chinese-language audiences.

## Reference(s):

- [Now Practice on ClawHub](https://clawhub.ai/perrykono-debug/skills/now-practice)
- [perrykono-debug publisher profile](https://clawhub.ai/user/perrykono-debug)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with JSON examples and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language practice content; frontend implementations may store completion records in browser localStorage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
