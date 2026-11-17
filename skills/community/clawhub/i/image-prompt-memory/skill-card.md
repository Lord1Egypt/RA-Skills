## Description:

Stores and retrieves successful image generation prompts by category, style, and keywords for quick reuse and recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acilgit](https://clawhub.ai/user/acilgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and image-generation workflow builders use this skill to save satisfactory image prompts, search them by category, style, or description, and reuse recommendations in later image creation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Successful prompts, feedback, and related metadata may persist sensitive personal, business, or confidential details in the local prompt-library JSON file.

Mitigation: Avoid saving sensitive prompt text, and periodically review or remove entries from the disclosed local JSON database.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acilgit/skills/image-prompt-memory)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown guidance and structured JSON prompt records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a local prompt-library JSON file at /root/.openclaw/workspace/data/prompt_library.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
