## Description: <br>
Dynamically dispatches tasks to architect, product manager, test expert, and solo coder roles, with multi-agent collaboration, consensus workflows, project lifecycle management, and Chinese-English bilingual support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiransoft](https://clawhub.ai/user/weiransoft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to route planning, architecture, testing, and implementation tasks to specialized agent roles. It also supports specification-driven development, code map generation, project understanding, progress tracking, and bilingual team workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill auto-activates broadly as a project workflow assistant and may affect normal agent behavior in a workspace. <br>
Mitigation: Install it only where a global project workflow assistant is desired, and review activation behavior before using it in shared or sensitive workspaces. <br>
Risk: Project-analysis and code-map features can scan local files and produce summaries that may expose sensitive project details if shared or committed. <br>
Mitigation: Run it only on trusted workspaces, avoid broad directories containing secrets, and review generated project-understanding and code-map files before sharing or committing them. <br>
Risk: The security review flags under-scoped local file scanning and write behavior, including unconstrained write paths in spec tooling. <br>
Mitigation: Constrain input paths, do not pass untrusted filenames to spec_tools.py, and review generated file changes before accepting them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weiransoft/multi-agent-team) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [MULTILINGUAL_GUIDE.md](artifact/MULTILINGUAL_GUIDE.md) <br>
- [USAGE_GUIDE.md](artifact/docs/guides/USAGE_GUIDE.md) <br>
- [SPEC.md](artifact/docs/spec/SPEC.md) <br>
- [PROJECT_STRUCTURE.md](artifact/docs/spec/PROJECT_STRUCTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON progress data, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese-English responses; may create project analysis, specification, code map, and progress files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
