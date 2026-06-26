## Description: <br>
GSD provides a complete workflow for taking projects from idea to execution through systematic planning, research, phase-based development, and verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oleg-schmidt](https://clawhub.ai/user/oleg-schmidt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use GSD to initialize projects, gather context, run research, create roadmaps and phase plans, execute implementation work, and verify results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct broad project changes, including automated file edits and commits. <br>
Mitigation: Use a dedicated branch or disposable workspace, review diffs before accepting changes, and require explicit approval before commits in shared repositories. <br>
Risk: The skill can propose package installs, global CLI installs, process kills, service starts, or deployments. <br>
Mitigation: Require explicit approval for installs, process management, deployments, and other environment-changing commands. <br>
Risk: The workflow may handle API keys or other secrets during setup and verification. <br>
Mitigation: Do not paste production API keys into chat; use local environment files or a secret manager and keep secrets out of generated documents. <br>
Risk: Generated plans, research, and verification notes can contain incorrect or misleading guidance. <br>
Mitigation: Review generated plans and verification evidence before execution, especially where the skill reports that runtime or manual testing is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oleg-schmidt/glittercowboy) <br>
- [GSD skill definition](artifact/SKILL.md) <br>
- [Planning configuration](artifact/references/planning-config.md) <br>
- [Checkpoint execution](artifact/references/checkpoint-execution.md) <br>
- [Git integration](artifact/references/git-integration.md) <br>
- [Verification patterns](artifact/references/verification-patterns.md) <br>
- [UI principles](artifact/references/ui-principles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, configuration snippets, and generated project planning files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .planning documents, modify project files, run commands, and produce verification notes depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
