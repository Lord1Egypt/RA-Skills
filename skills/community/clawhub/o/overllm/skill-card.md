## Description:

Overllm helps agents audit Python and JavaScript/TypeScript codebases for unnecessary LLM API calls that can be replaced with deterministic code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theadamdanielsson](https://clawhub.ai/user/theadamdanielsson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to run overllm against source files, review structured findings, and identify model calls that can be replaced by regexes, standard library functions, batching, or other deterministic code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and execute the overllm command-line tool.

Mitigation: Install overllm only from a trusted package index and prefer an isolated virtual environment or container.

Risk: Opt-in modes such as --fix and --write-baseline can modify source or baseline files.

Mitigation: Run read-only scans first, review findings, and use preview or diff behavior before enabling write modes.

## Reference(s):

- [Overllm project homepage](https://github.com/theadamdanielsson/overllm)
- [ClawHub skill page](https://clawhub.ai/theadamdanielsson/skills/overllm)
- [ClawHub publisher profile](https://clawhub.ai/user/theadamdanielsson)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or text with inline shell commands and structured finding summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal scans are read-only; opt-in fix and baseline modes can write files.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
