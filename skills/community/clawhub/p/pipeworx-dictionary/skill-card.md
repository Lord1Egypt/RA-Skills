## Description:

Word definitions, phonetics, usage examples, synonyms, and antonyms from the Free Dictionary API

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up English word meanings, phonetics, usage examples, synonyms, and antonyms for writing, vocabulary, flashcard, and language-learning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup runs an unpinned npm package that can change after review.

Mitigation: Pin the mcp-remote version or run the MCP configuration in a constrained environment before trusting it.

Risk: Dictionary lookups may send submitted words or phrases to an external service.

Mitigation: Do not submit secrets, internal project names, or sensitive text through this skill.

## Reference(s):

- [Pipeworx Dictionary Pack](https://pipeworx.io/packs/dictionary)
- [Pipeworx Dictionary MCP Endpoint](https://gateway.pipeworx.io/dictionary/mcp)
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/skills/pipeworx-dictionary)
- [Publisher Profile](https://clawhub.ai/user/brucegutman)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dictionary responses may include grouped definitions, phonetics, examples, synonyms, antonyms, and audio pronunciation URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
