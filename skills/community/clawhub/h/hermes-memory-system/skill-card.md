## Description: <br>
Hermes helps OpenClaw agents persist memory across sessions, manage automatic memory sync, and generate reusable skills from task trajectories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add cross-session memory, task trajectory capture, skill candidate generation, and optional data export to an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to persist conversation history, tool activity, file-operation context, and generated skill candidates. <br>
Mitigation: Install it only when persistent OpenClaw memory is intended, and review or redact memory, trajectory, export, log, and diagnostic files before sharing them. <br>
Risk: Automatically generated skill candidates may contain incorrect, sensitive, or unsuitable instructions. <br>
Mitigation: Keep production approval required and auto-install disabled so generated skills are reviewed before use. <br>
Risk: Sensitive stored data may remain readable if encryption is not configured. <br>
Mitigation: Set real encryption where supported and keep optional data export disabled unless there is a defined operational need. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/hermes-memory-system) <br>
- [ClawHub package homepage](https://clawhub.ai/skills/hermes-agent-skill) <br>
- [CHANGELOG.md](references/CHANGELOG.md) <br>
- [DEPLOYMENT_GUIDE.md](references/DEPLOYMENT_GUIDE.md) <br>
- [TEST_GUIDE.md](references/TEST_GUIDE.md) <br>
- [VERSION_MANAGEMENT.md](references/VERSION_MANAGEMENT.md) <br>
- [ACCEPTANCE_TEST_PLAN.md](references/ACCEPTANCE_TEST_PLAN.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory, trajectory, skill candidate, export, log, and diagnostic files in the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, artifact _meta.json, and references/CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
