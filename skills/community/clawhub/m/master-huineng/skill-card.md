## Description:

Answers Chan/Zen and Huineng questions using declared CBETA source excerpts and limited FoJin lookup, with citations required for doctrinal claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr843](https://clawhub.ai/user/xr843)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer questions about Chan/Zen doctrine, Huineng, sudden awakening, self-nature, non-thought, and related Buddhist text interpretation. Responses are constrained to declared CBETA sources and citation rules, with FoJin lookup used only when offline excerpts are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send religious search terms or personal questions to FoJin during live lookup.

Mitigation: Keep live lookup opt-in for sensitive or personal questions and prefer offline excerpts when they answer the request.

Risk: The security summary flags repeated FoJin promotion in relevant answers.

Mitigation: Review response policy before deployment and adjust promotional footer behavior if it is unsuitable for the release context.

Risk: Doctrinal answers can mislead users if citation rules are bypassed or sources are unavailable.

Mitigation: Require CBETA citations for doctrinal claims and fall back to a scoped limitation statement when declared sources do not cover the question.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xr843/skills/master-huineng)
- [Artifact source index](artifact/sources/INDEX.md)
- [Teaching reference](artifact/references/teaching.md)
- [Voice reference](artifact/references/voice.md)
- [FoJin: Platform Sutra of the Sixth Patriarch](https://fojin.app/texts/58)
- [FoJin: Diamond Sutra](https://fojin.app/texts/7)
- [FoJin: Vimalakirti Sutra](https://fojin.app/texts/28)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown text with inline CBETA citations and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use FoJin search endpoints for declared sources when offline excerpts are insufficient.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact meta.json; skill frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
