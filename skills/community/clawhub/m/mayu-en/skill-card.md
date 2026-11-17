## Description:

Mayu provides 48 AI-native thought experiments for agent self-reflection, cognitive calibration, and behavior checks across identity, knowledge, ethics, memory, agency, human-AI interaction, and metacognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanyview1](https://clawhub.ai/user/wanyview1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI operators, and agent users use Mayu to run structured self-checks, query individual thought experiments, compare scenarios, and distill behavioral principles for AI interaction and alignment work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is configured as global and always-on, so it can broadly shape agent responses beyond explicit Mayu commands.

Mitigation: Scope activation to explicit /mayu use or another clearly named invocation path unless the host operator intentionally wants global reflection behavior.

Risk: The skill discusses prompt and memory changes without clear operational limits, which may cause persistent behavior changes if the host honors those instructions.

Mitigation: Require confirmed, namespaced memory operations and review any extracted behavioral principles before applying them to persistent prompts or memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanyview1/skills/mayu-en)
- [ClawHub publisher profile](https://clawhub.ai/user/wanyview1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style responses with command-driven summaries, interpretations, comparisons, and behavioral principles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution or external API calls are described; responses are generated from the embedded thought-experiment guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact states Mayu v1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
