## Description:

Tarot draw and reading for Mystilink: draws upright or reversed cards for a spread, then supports interpretation with Wiki card pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystilink-ai](https://clawhub.ai/user/mystilink-ai)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to run tarot draws, accept user-provided cards, and prepare concise readings tied to a question and spread. It is appropriate for tarot questions, spread selection, and card-meaning support, with medical and legal certainty out of scope.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Wiki lookups may disclose card-related query data and locale to the remote lookup service.

Mitigation: Avoid sending private health, legal, financial, relationship, or similarly sensitive details in Wiki lookup queries unless the user accepts that sharing.

Risk: Tarot readings can be mistaken for deterministic advice in sensitive decisions.

Mitigation: Keep readings reflective and entertainment-oriented, and do not claim medical or legal certainty.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mystilink-ai/skills/mystilink-tarot-skill)
- [Server-Resolved GitHub Source](https://github.com/mystilink-ai/mystilink-tarot-skill)
- [tarot - skill reference](references/overview.md)
- [Draw method](references/method-draw.md)
- [Mystilink Wiki search API](https://wiki.mystilink.com/api/v1/search?q=The+Fool&system=tarot&locale=en)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; the draw script emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Wiki lookups can add cited card-page context when network access is available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
