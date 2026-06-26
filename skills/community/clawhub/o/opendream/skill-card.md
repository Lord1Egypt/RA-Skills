## Description: <br>
OpenDream configures an OpenClaw or Hermes agent to run an overnight dream process that reads daily memory context, writes dream cycle files, and reports morning recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajaylakhani](https://clawhub.ai/user/ajaylakhani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use OpenDream to add a scheduled overnight reflection workflow to an OpenClaw or Hermes agent. The skill configures heartbeat behavior, dream prompt fragments, dream output files, and validation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes persistent heartbeat scheduling and agent prompt/configuration files. <br>
Mitigation: Review the setup diff before installation, especially HEARTBEAT.md, SOUL.md, and openclaw.json, and keep or inspect the generated backups. <br>
Risk: Recurring overnight processing can reflect local daily memory content in generated dream files. <br>
Mitigation: Treat files written under dreams/ as potentially sensitive and apply the same access controls and retention practices used for local memory files. <br>
Risk: Existing agents.defaults.heartbeat settings may be replaced by the dream heartbeat configuration. <br>
Mitigation: Compare the current heartbeat block with assets/openclaw.json before running setup.py, and merge manually if existing heartbeat behavior must be preserved. <br>


## Reference(s): <br>
- [ClawHub OpenDream release page](https://clawhub.ai/ajaylakhani/opendream) <br>
- [OpenDream Technical Reference](references/REFERENCE.md) <br>
- [OpenDream Manual Installation](references/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recurring dream cycle Markdown files under dreams/YYYY-MM-DD/ and a morning-recall Markdown file when installed and scheduled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; SKILL.md frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
