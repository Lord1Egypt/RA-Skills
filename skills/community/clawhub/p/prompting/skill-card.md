## Description:

Write, test, and iterate prompts for AI models with voice preservation, model-specific adaptation, and systematic failure analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, operators, and content teams use this skill to create, test, and refine prompts across AI models while preserving user voice and diagnosing failures such as hallucination, format drift, refusal, verbosity, and weak variation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent local prompting memory that may store style notes, corrections, and prompt history.

Mitigation: Review the contents of ~/prompting regularly, avoid storing secrets or sensitive samples, and delete the folder or individual files when persistence is no longer wanted.

Risk: The skill includes unsafe prompt-priority advice about user messages overriding system prompts.

Mitigation: Follow the host agent's instruction hierarchy and treat this skill's advice as lower-priority task guidance only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/prompting)
- [Prompt failure modes](artifact/failures.md)
- [Prompt iteration workflow](artifact/iteration.md)
- [Prompting memory setup](artifact/memory-template.md)
- [Model-specific quirks](artifact/models.md)
- [Advanced prompting techniques](artifact/techniques.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands]

**Output Format:** [Markdown with concise prompt guidance, examples, and occasional shell commands for local setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local prompting memory files under ~/prompting for user preferences, prompt patterns, and prompt history.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
