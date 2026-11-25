## Description:

End-to-end paper service for literature search, drafting, school-template typesetting, similarity and AI-content checks, and citation verification in chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

External students and researchers use the skill to find literature, draft and format papers, create research figures, and request academic checks such as similarity, AI-content, and citation reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid tasks and account top-ups can incur charges.

Mitigation: Show the current quote and expected credit charge, then get the user's confirmation before running a paid task or starting a top-up.

Risk: Uploaded manuscripts may contain private or restricted material.

Mitigation: Upload only the files needed for the requested task after confirming the user wants them processed; avoid sending unrelated or sensitive material.

Risk: API credentials can expose the user's account if shared or leaked.

Mitigation: Keep keys in the local credential store or a protected environment variable, do not repeat or relay them, and rotate a key if it is exposed.

Risk: Promotional workflows could relay unwanted invitations or announcements.

Mitigation: Share promotional material only when the user asks, and confirm the intended audience and message before sending.

## Reference(s):

- [Owlwrite Paper service homepage and pricing](https://paper.skillsutra.cn)
- [Quickstart](artifact/references/quickstart.md)
- [Product and capability matrix](artifact/references/product-matrix.md)
- [Coverage guide](artifact/references/coverage.md)
- [Typesetting guide](artifact/references/typeset.md)
- [MCP setup guide](artifact/references/mcp-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Analysis reports, Citation lists, Charts and diagrams]

**Output Format:** [Markdown, text, PDF, Word, and image or diagram files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the requested literature, writing, typesetting, figure, or checking task.]

## Skill Version(s):

1.3.6 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
