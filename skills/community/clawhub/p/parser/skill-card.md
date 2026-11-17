## Description:

Parse JSON, CSV, XML, and logs into structured output. Use when converting formats, validating structure, extracting fields, analyzing nested data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to parse, validate, filter, split, extract, and summarize local JSON, CSV, XML, YAML, log, and text files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The parser reads local files supplied by the user.

Mitigation: Use it only with files you intend to parse and are comfortable exposing to the local tool process.

Risk: Pattern arguments for grep-like parsing may have option-injection edge cases.

Mitigation: Review commands before execution and prefer hardened argument handling such as placing '--' before user-supplied patterns.

Risk: The skill creates a local data directory that is not clearly used by the parser behavior.

Mitigation: Document or remove the directory creation before deployment in controlled environments.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [Parser on ClawHub](https://clawhub.ai/ckchzh/skills/parser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected parser command and may include structured JSON, extracted text, filtered lines, CSV tables, XML snippets, YAML values, split fields, or file statistics.]

## Skill Version(s):

3.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
