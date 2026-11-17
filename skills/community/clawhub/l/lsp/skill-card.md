## Description:

Multi-language code navigation via persistent LSP daemons for definitions, references, hover information, symbols, diagnostics, completions, signature help, and rename previews across common programming languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamnaghs](https://clawhub.ai/user/adamnaghs)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to navigate codebases through installed language servers, including finding definitions and references, reading hover/type information, listing symbols, checking diagnostics, and previewing rename edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local background daemon reads queried source files and sends them to installed language servers.

Mitigation: Use the skill only in workspaces where local language servers are trusted to receive the queried source files.

Risk: The LSP_SERVER environment variable can replace the language server command with another executable that receives source file contents.

Mitigation: Keep LSP_SERVER unset unless intentionally pointing it at a trusted executable.

Risk: A system-wide symlink can broaden who invokes or modifies the installed command.

Mitigation: Prefer direct invocation or a user-writable PATH location over a system-wide symlink.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adamnaghs/skills/lsp)
- [Eclipse JDT Language Server](https://github.com/eclipse-jdtls/eclipse.jdt.ls)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-formatted command output from LSP queries and setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and at least one installed language server for queried languages.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
