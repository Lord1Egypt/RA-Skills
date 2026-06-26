## Description: <br>
InkOS is an autonomous fiction-writing CLI agent with a local web workbench for generating, continuing, auditing, revising, analyzing, and exporting novels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[narcooo](https://clawhub.ai/user/narcooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and external agents use this skill to operate InkOS for creative fiction projects, including novel generation, chapter continuation, style imitation, fan fiction workflows, quality auditing, analytics, and export. It is useful when an agent needs concrete InkOS CLI commands, configuration guidance, or workflow sequencing for long-form writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: InkOS uses LLM provider credentials and can send project content to the configured provider endpoint. <br>
Mitigation: Use API keys through environment variables, keep project folders private, and configure only trusted provider or proxy URLs. <br>
Risk: Project configuration, logs, books, story state, and memory files may contain sensitive manuscript or credential-adjacent data. <br>
Mitigation: Add inkos.json, logs, books, story state, and memory files to .gitignore and avoid publishing project directories. <br>
Risk: InkOS Studio exposes project controls through a local web UI. <br>
Mitigation: Run Studio only on a trusted local machine and do not expose it beyond localhost. <br>
Risk: Rename, replace, rewrite, delete, import, and daemon workflows can substantially change local writing projects. <br>
Mitigation: Make backups before destructive or long-running workflows and review resulting changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/narcooo/inkos) <br>
- [InkOS GitHub Homepage](https://github.com/Narcooo/inkos) <br>
- [InkOS npm Package](https://www.npmjs.com/package/@actalk/inkos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-capable CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or modification of local project files, logs, story state, exports, and InkOS Studio workflows.] <br>

## Skill Version(s): <br>
2.3.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
