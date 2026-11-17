## Description:

The skill helps an agent answer questions about Atiśa, Kadam teachings, lamrim foundations, and bodhicitta in a concise, citation-rich style with explicit doctrinal source boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr843](https://clawhub.ai/user/xr843)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer learning-oriented questions about Atiśa, Kadam school topics, three scopes practice, and bodhicitta. It guides answers toward declared Tibetan canonical and Kadam sources, while refusing esoteric practice instruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send doctrinal search terms or parts of a user's question to the external FoJin service when local sources are insufficient.

Mitigation: Use the offline sources first, avoid including private or confidential details in questions, and ask the agent to stay offline for sensitive requests.

Risk: Religious teaching answers can be misleading if doctrinal claims are not tied to the declared source corpus.

Mitigation: Require citations from the declared Tibetan canonical or Kadam sources for doctrinal claims and remove unsupported claims before answering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xr843/skills/master-atisha)
- [Publisher profile](https://clawhub.ai/user/xr843)
- [SKILL.md](artifact/SKILL.md)
- [Teaching reference](artifact/references/teaching.md)
- [Voice reference](artifact/references/voice.md)
- [Sources index](artifact/sources/INDEX.md)
- [Bodhipathapradipa excerpts](artifact/sources/bodhipathapradipa-excerpts.md)
- [84000](https://84000.co)
- [FoJin content search API](https://fojin.app/api/search/content)
- [FoJin semantic search API](https://fojin.app/api/search/semantic)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with inline canonical citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are expected to cite declared Tibetan canonical or Kadam sources for doctrinal claims and to refuse esoteric practice instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
