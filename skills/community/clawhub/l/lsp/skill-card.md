## Description: <br>
LSP Code Navigation gives agents multi-language code navigation through persistent Language Server Protocol daemons for definitions, references, hover information, symbols, diagnostics, completions, signatures, and rename previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdamNaghs](https://clawhub.ai/user/AdamNaghs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill to inspect source code with language-server semantics across Python, TypeScript/JavaScript, Rust, Go, C/C++, Bash, Java, CSS, HTML, and JSON workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local language-server binaries and a short-lived daemon against the user's workspace. <br>
Mitigation: Install only trusted or pinned language servers, use the skill in trusted workspaces, and run the shutdown command when the daemon should stop. <br>
Risk: Environment variables such as LSP_SERVER and LSP_SOCK can change which command runs or which socket is used. <br>
Mitigation: Do not let untrusted projects or wrappers set LSP_SERVER or LSP_SOCK before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AdamNaghs/lsp) <br>
- [Eclipse JDT Language Server](https://github.com/eclipse-jdtls/eclipse.jdt.ls) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and command-line output with Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+ and at least one trusted language-server binary for the target language.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
