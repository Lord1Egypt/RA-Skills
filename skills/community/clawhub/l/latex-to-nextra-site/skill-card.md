## Description:

Converts project-cookbook-latex LaTeX projects into Chinese Nextra documentation sites while preserving PlantUML, Draw.io, Mermaid diagrams, code blocks, LaTeX formulas, and tables, and producing deployable project folders for GitHub, Vercel, Docker, or self-hosting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samonysh](https://clawhub.ai/user/samonysh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to convert chaptered Chinese LaTeX cookbook, ebook, or paper projects into Nextra v3 documentation sites. It is intended for preserving technical content such as diagrams, formulas, tables, and code while preparing a deployable web documentation project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated build and diagram-rendering scripts may run unintended local commands when used on untrusted projects.

Mitigation: Review and adjust generated scripts before execution, replace shell-based execSync Docker commands with argument-array execution, and validate diagram filenames.

Risk: Containerized diagram rendering or builds may expose local files or secrets if source mounts, networking, or build contexts are too broad.

Mitigation: Pin the PlantUML image by digest, use read-only source mounts and restricted networking where possible, and avoid copying token-bearing .npmrc files into Docker builds.

Risk: LaTeX shell escape can execute commands from document content.

Mitigation: Keep shell escape disabled by default and enable it only with explicit user consent in a sandboxed environment for trusted content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samonysh/skills/latex-to-nextra-site)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, shell commands, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Nextra/Next.js documentation project structure with deployment and validation steps.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
