## Description: <br>
Analyzes OpenClaw version updates before upgrade, checks potential configuration impact, generates a compatibility report, and backs up affected files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adgai115](https://clawhub.ai/user/adgai115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and maintainers use this skill before upgrading to review release-note impact, identify configuration areas that may need attention, generate an upgrade impact report, and preserve affected files in a backup directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports and backups may include workspace configuration details. <br>
Mitigation: Review generated files before sharing or committing them, and run the skill only in workspaces where report and backup writes are acceptable. <br>
Risk: The documentation includes an upgrade command example even though the skill is primarily advisory. <br>
Mitigation: Treat the skill as an assessment and backup tool; run any OpenClaw upgrade command separately and only after explicit operator approval. <br>
Risk: The skill requests exec capability in metadata while its intended workflow is analysis, reporting, and backup. <br>
Mitigation: Install with the least permissions practical for the environment and review any command execution request before allowing it to modify the host installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adgai115/openclaw-upgrade-assistant) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw GitHub releases](https://github.com/openclaw/openclaw/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown report, console text, JSON-like analysis objects, and backup manifest files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an impact report and backup manifest into the workspace when configured to generate reports or backups.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
