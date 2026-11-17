## Description:

Create and manage LLM-powered personal knowledge bases using Karpathy's wiki method.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinchengcool](https://clawhub.ai/user/gavinchengcool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to create and maintain Obsidian-compatible markdown vaults for ingesting sources, organizing concepts and entities, answering questions from saved notes, and preserving useful outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent project files and can copy local files into a vault.

Mitigation: Use explicit commands, review source paths before ingestion, avoid sensitive local paths, and keep output paths constrained to the intended vault.

Risk: The skill can fetch URLs and ingest web content into the knowledge base.

Mitigation: Review each URL before ingestion and treat fetched content as untrusted source material until summarized and verified.

Risk: The security summary flags broad triggers and unsafe URL or file ingestion instructions as requiring careful review before installation.

Mitigation: Review the skill before deployment and require safe argument handling instead of literal shell interpolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gavinchengcool/skills/llm-kb)
- [ClawHub publisher profile](https://clawhub.ai/user/gavinchengcool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates plain markdown vault files, Obsidian configuration files, source cards, concept pages, entity pages, output pages, and activity logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
