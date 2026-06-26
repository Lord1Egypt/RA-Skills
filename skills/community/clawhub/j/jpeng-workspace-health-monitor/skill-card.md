## Description: <br>
Performs comprehensive workspace health checks including disk usage, file counts, skill health, large files, and empty directories with actionable recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to inspect a local workspace for disk usage, skill health, large files, empty directories, and maintenance recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recursively inspects local workspace metadata, so file and folder names from sensitive or overly broad directories may appear in reports or agent context. <br>
Mitigation: Run it only against the intended workspace and avoid broad home, system, or sensitive directories when names should remain private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-workspace-health-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [JavaScript object for health metrics and a Markdown-formatted workspace health report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local file and directory metadata, health scores, status levels, and actionable recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
