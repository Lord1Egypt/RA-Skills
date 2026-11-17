## Description:

Provides a Chinese idiom dictionary with search, listing, random idiom selection, and documented language-learning commands for stories, chain play, quizzes, usage examples, and category browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and browse Chinese idioms for language learning, writing support, examples, and lightweight command-line lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled command behaves as a generic local data logger and persistently records command arguments, which is broader than the documented idiom dictionary behavior.

Mitigation: Review commands before execution, avoid passing secrets as command arguments, and keep IDIOM_DICTIONARY_DIR pointed at a private user-owned directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/idiom-dictionary)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required; some bundled utility commands can write persistent local files under the configured idiom-dictionary data directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
