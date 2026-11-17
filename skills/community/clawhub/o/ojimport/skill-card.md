## Description:

Imports programming contest problems from OJ platforms such as AtCoder and Codeforces into standardized problem packages, or generates test data from user-provided problem statements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and competitive programming problem maintainers use this skill to convert imported or supplied OJ problem statements into standardized problem packages. It can produce problem Markdown, YAML configuration, C++ reference solutions, generated test data, audit guidance, and packaged ZIP deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can delete, rename, zip, compile, or run files in Desktop work directories.

Mitigation: Use a controlled workspace and require path validation plus confirmation before any rm, mv, zip, compile, or run step.

Risk: Imported problem text, titles, IDs, and URLs are untrusted inputs that can influence generated files and commands.

Mitigation: Validate and sanitize problem identifiers, titles, source URLs, filenames, and resolved paths before writing files or executing commands.

Risk: Generated C++ reference solutions and test-data generators are executable code.

Mitigation: Review generated source files before compiling or running them, preferably in a sandbox or disposable problem workspace.

## Reference(s):

- [Test Data Design Reference](artifact/references/testdata-design.md)
- [ClawHub Skill Page](https://clawhub.ai/fslong520/skills/ojimport)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown instructions with C++ source files, YAML configuration, generated test data files, and ZIP packages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-oriented deliverables and may compile, run, clean, and package generated artifacts during the workflow.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
