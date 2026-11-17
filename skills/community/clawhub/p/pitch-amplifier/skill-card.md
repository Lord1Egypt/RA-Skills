## Description:

Turn a vague reporting clue, observation, or topic hunch into a deeper news pitch by extracting entities, retrieving 1-2 hop context from a city knowledge graph, and generating an editor-style planning memo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangzuomin2019](https://clawhub.ai/user/huangzuomin2019)

### License/Terms of Use:

MIT-0

## Use Case:

Journalists, editors, and reporting teams use this skill to expand early local-news clues into graph-grounded pitch memos with issue context, story angles, and interview targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive reporting clues, source identities, allegations, or local graph contents may be sent to an external LLM provider when API keys are present.

Mitigation: Run without OPENAI_API_KEY or GLM_API_KEY for confidential work, or obtain explicit approval for remote LLM processing before use.

Risk: Generated pitch memos may reflect incomplete graph coverage or weak graph recall.

Mitigation: Treat weak graph coverage as a reporting gap and verify angles, entities, and interview targets before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangzuomin2019/skills/pitch-amplifier)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Shell commands, Guidance]

**Output Format:** [Markdown planning memo with extracted entities and graph context printed in the terminal]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local city knowledge graph and, when configured with OPENAI_API_KEY or GLM_API_KEY, an external LLM provider.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
