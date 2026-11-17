## Description:

Answer questions with live web search and cited sources using a Grok model through the Grokified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imfaisii](https://clawhub.ai/user/imfaisii)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users research current public information and receive answers with citations, optionally limiting searches to selected domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research questions and the API key are sent to Grokified.

Mitigation: Use only public, non-sensitive questions; never include secrets, personal data, private code or confidential information.

Risk: Search-generated answers may misread or misrepresent cited pages.

Mitigation: Check important facts against the original cited sources before relying on them.

## Reference(s):

- [Grokified model documentation](https://grokified.com/docs/models)
- [Grokified agent tools documentation](https://grokified.com/docs/agent-tools)
- [Grokified web research on ClawHub](https://clawhub.ai/imfaisii/skills/grokified-web-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Short answer and findings with inline citations and a sources list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search can be restricted to up to five domains; important facts require independent source verification.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
