## Description:

A Chinese-language research pipeline that moves a topic through scope definition, literature discovery, synthesis, experiment design, analysis, and paper drafting with human confirmation between phases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and OpenClaw users use this skill to turn an initial research topic into staged Markdown research artifacts and a draft academic paper. It is intended for workflows where a human reviews each phase before the next phase proceeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics, prompts, and generated notes may be sent to the configured OpenClaw LLM provider.

Mitigation: Use only environments approved for the research data, and avoid confidential or proprietary topics unless that provider and environment are authorized.

Risk: Generated research outputs are persisted under the OpenClaw knowledge-base path.

Mitigation: Review output locations, access controls, and retention before running the pipeline on sensitive topics.

Risk: Obsidian integration is optional and may not automatically sync results in every environment.

Mitigation: Treat Obsidian export as a manual follow-up unless the local Obsidian command is installed and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-research-pipeline)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown files and terminal prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates staged research notes, a paper draft, and a log under the configured OpenClaw knowledge-base path.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
