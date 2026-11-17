## Description:

Access diverse jokes by category, language, and type with filters for safe content using the free JokeAPI without requiring registration or an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djttt](https://clawhub.ai/user/djttt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch random or filtered jokes from JokeAPI, including categories, languages, response formats, safe-mode filtering, and blacklist filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-invoked requests are sent to JokeAPI, including any text provided with --contains.

Mitigation: Use the skill only when external JokeAPI requests are acceptable for the task and avoid sending sensitive text in search filters.

Risk: Jokes returned by JokeAPI may include content unsuitable for workplace or public contexts.

Mitigation: Use --safe-mode or blacklist filters such as nsfw, religious, political, racist, sexist, and explicit when output may be shared.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/djttt/skills/joke-api)
- [JokeAPI Documentation](https://jokeapi.dev/)
- [JokeAPI GitHub Repository](https://github.com/Sv443-Network/JokeAPI)
- [JokeAPI Status Page](https://status.sv443.net/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text, JSON, XML, YAML, or Markdown with inline shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the external JokeAPI service and can apply safe-mode, blacklist, category, language, type, amount, and text-search filters.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
