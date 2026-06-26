## Description: <br>
A Chinese-language multi-agent workflow skill for planning, drafting, reviewing, and refining web-novel projects with reusable templates, quality rules, and shell workflow scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[micromsf](https://clawhub.ai/user/micromsf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agent operators use this skill to set up a structured novel project, coordinate specialized writing agents, generate planning documents and chapter drafts, and review output against quality and content rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enforces strict editorial content redlines and quality gates that may reject otherwise acceptable creative choices. <br>
Mitigation: Review and adapt the bundled content redline, workflow, and scoring rules before using the skill for a specific publication context. <br>
Risk: The workflow includes AI-style cleanup and production guidance for generated fiction. <br>
Mitigation: Represent AI assistance honestly in any commercial or disclosure-sensitive publication process. <br>
Risk: The shell scripts create and overwrite project template files in the target project directory. <br>
Mitigation: Run the scripts in a dedicated project directory and review generated files before integrating them into an existing manuscript workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/micromsf/novel-multi-agent-skill) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [Content review redlines](artifact/rules/内容审查红线.md) <br>
- [Quality scoring standard](artifact/rules/质量评分标准.md) <br>
- [Collaboration workflow standard](artifact/rules/协作流程规范.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown project documents, shell workflow commands, and agent coordination guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project setup files, planning templates, chapter draft templates, review report templates, and workflow prompts for configured OpenClaw agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
