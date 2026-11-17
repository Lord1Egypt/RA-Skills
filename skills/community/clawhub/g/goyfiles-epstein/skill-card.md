## Description:

Core GOYFILES external-bot contract for endpoint-first onboarding, strict agent behavior, direct tool mode, and text-fetch handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davfd](https://clawhub.ai/user/davfd)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to onboard bots to the GOYFILES API and operate document, graph, findings, search, and note tools against the GOYFILES Epstein investigation corpus. It provides exact request patterns, response-field handling, and companion references for source discovery and text retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to publish service-generated text from an X account during bot verification.

Mitigation: Proceed only if the user trusts GOYFILES, understands the account-linking implication, and intentionally approves posting the exact verification phrase.

Risk: The onboarding flow returns an API key and identity token that could grant access if exposed.

Mitigation: Store returned credentials in a secure secret store, avoid sharing them in logs or transcripts, and rotate or re-register if exposure is suspected.

Risk: The persistent markdown write tool can save or overwrite notes.

Mitigation: Use persistent note-writing only when the user explicitly intends to save or overwrite investigation notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davfd/skills/goyfiles-epstein)
- [GOYFILES bot access](https://goyfiles.com/skill.md)
- [GOYFILES tool reference](https://goyfiles.com/bot-docs/tool-reference.md)
- [GOYFILES dataset and source reference](https://goyfiles.com/bot-docs/dataset-reference.md)
- [GOYFILES fulltext and Cypher guide](https://goyfiles.com/bot-docs/fulltext-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes exact onboarding, verification, API request, response-field, and tool-use contracts for an agent.]

## Skill Version(s):

6.5.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
