## Description: <br>
Runs a Python-based operations inspection that checks local host resources and detected middleware, then reports Kubernetes, log, and business indicators with documented hybrid or simulated sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations engineers and DevOps teams can use this skill to run local health checks across system resources, detected middleware, container, log, and business-metric layers. It is best suited for preliminary inspection reports and should not be treated as authoritative production monitoring without replacing simulated sections with real data collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some default report sections can contain simulated operational findings. <br>
Mitigation: Label simulated or hybrid sections clearly and replace them with real data collection before using the output for production decisions. <br>
Risk: Exported inspection reports may contain sensitive environment or service details. <br>
Mitigation: Review report contents, file permissions, retention, and sharing paths before enabling --export or scheduled runs. <br>
Risk: Several checks require elevated host, service, or network visibility. <br>
Mitigation: Run with the least privileges needed for the selected layers and document which checks are skipped when dependencies or permissions are missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-patrol-2026) <br>
- [README.md](artifact/README.md) <br>
- [README_INSPECTION.md](artifact/README_INSPECTION.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [skill.json](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Console text with optional JSON report file export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When --export is used, the script writes an inspection_report_*.json file in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
