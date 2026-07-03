## Description: <br>
Git-like version control for AI prompts: track changes, A/B test variants, measure metrics, rollback with confidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prompt engineers use this skill to set up and operate a local prompt versioning workflow for tracking prompt YAML files, comparing versions, testing variants, rolling back, and generating reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill overstates evaluation and sync features, which could mislead users managing production prompts. <br>
Mitigation: Do not rely on its A/B test quality scores, confidence labels, semantic summaries, or remote-sync guidance for production decisions unless they are replaced with real evaluation and clearly configured git workflows. <br>
Risk: Prompt files and test data may contain proprietary business logic or sensitive examples that could be exposed through shared repositories. <br>
Mitigation: Review the .prompt contents and remote settings before sharing, and use synthetic or anonymized test data for versioned prompt evaluation. <br>


## Reference(s): <br>
- [Prompt Version Control on ClawHub](https://clawhub.ai/harrylabsj/prompt-version-control) <br>
- [Default prompt repository configuration](references/config.yaml) <br>
- [Prompt Version Control input schema](schemas/input.schema.json) <br>
- [Prompt Version Control output schema](schemas/output.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, YAML configuration examples, JSON schemas, and CLI output summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI workflow creates local .prompt files when commands are run; test metrics and semantic summaries should be treated as demonstration support unless connected to real evaluation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
