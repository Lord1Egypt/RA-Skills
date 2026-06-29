## Description: <br>
latex-modular helps agents assemble, refactor, validate, and convert modular LaTeX documents using reusable components and local Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to generate, modularize, refactor, and validate LaTeX documents, especially LuaLaTeX/XeLaTeX projects with reusable preamble, command, environment, table, graphics, and style components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify local LaTeX or project files through write, delete, refactor, and inject workflows. <br>
Mitigation: Use a dedicated workspace, keep backups, and verify output paths before running write, delete, refactor, or inject modes. <br>
Risk: The skill can run a local LaTeX compiler on generated or user-provided .tex files. <br>
Mitigation: Avoid compiling untrusted .tex files on a main machine unless the compiler is sandboxed and automatic package installation and shell escape are disabled. <br>
Risk: The security scan flags a mismatch between local file modification and compiler execution behavior and the declared low permission posture. <br>
Mitigation: Review the skill and its permissions before deployment, especially in shared or production workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/latex-modular) <br>
- [Guide](artifact/references/guide.md) <br>
- [Architecture](artifact/references/architecture.md) <br>
- [Component specification](artifact/references/component-spec.md) <br>
- [Permissions](artifact/references/permissions.md) <br>
- [Changelog](artifact/references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated LaTeX or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local .tex files, conversion reports, validation reports, component files, and optional PDFs when a LaTeX engine is available.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter, release metadata, changelog released 2026-06-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
