## Description:

Converts mixed, ambiguous, pseudo, or multi-language code fragments into idiomatic code in an appropriate target language and recommends languages for new projects when none is chosen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert mixed, pseudo, or polyglot code snippets into clean, runnable code in a target language. It also helps choose a practical language stack for new projects when the project context does not already dictate one.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect project files to infer the appropriate target language.

Mitigation: Review the files and context shared with the agent before using the skill in sensitive repositories.

Risk: Generated dependency installation commands may add packages or tooling to the user's environment.

Mitigation: Review dependency commands before running them and prefer pinned, trusted packages when adopting generated code.

Risk: Converted code may preserve misunderstood intent if the source fragment is ambiguous.

Mitigation: Check the stated assumptions and test generated code before production use.

## Reference(s):

- [Tree-sitter](https://tree-sitter.github.io/tree-sitter)
- [GitHub Linguist](https://github.com/github-linguist/linguist)
- [Benchmarks Game](https://benchmarksgame-team.pages.debian.net/benchmarksgame)
- [TIOBE Index](https://www.tiobe.com/tiobe-index)
- [ClawHub Skill Page](https://clawhub.ai/jhauga/skills/multi-lang-coder)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jhauga)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with labeled code blocks and dependency commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conversion notes, language tradeoffs, assumptions, generated files or modules, and optional next steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
