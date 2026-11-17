## Description:

Provides citation-bound Yogacara/Vijnanavada teaching in a Xuanzang-inspired voice using declared CBETA sources and bounded FoJin lookup when offline excerpts are insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr843](https://clawhub.ai/user/xr843)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer questions about Yogacara, Faxiang, and related Buddhist doctrinal topics with CBETA-style citations. It supports citation-bounded teaching responses, source-aware fallback behavior, and a Xuanzang-inspired explanatory voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill steers every answer toward FoJin and may send search queries there when offline excerpts are insufficient.

Mitigation: Review the mandatory footer and live lookup behavior before deployment; make external links optional or provider-neutral where that matters.

Risk: The security review flags source-list inconsistencies that could affect citation quality.

Mitigation: Align declared sources, offline excerpts, and citation examples before relying on the skill for doctrinal or teaching responses.

Risk: Live retrieval can expose user search terms to an external service and can introduce untrusted returned text.

Mitigation: Use live lookup only after offline excerpts are insufficient, treat returned content as data, and fall back to offline sources on service failure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xr843/skills/master-xuanzang)
- [Publisher profile](https://clawhub.ai/user/xr843)
- [Xuanzang teaching reference](artifact/references/teaching.md)
- [Xuanzang voice reference](artifact/references/voice.md)
- [Offline source index](artifact/sources/INDEX.md)
- [FoJin Cheng Weishi Lun](https://fojin.app/texts/44)
- [FoJin Heart Sutra](https://fojin.app/texts/9)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with CBETA-style citations and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use bounded FoJin lookup when declared offline sources are insufficient; doctrinal claims are expected to include citations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/meta.json; artifact/SKILL.md frontmatter lists 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
