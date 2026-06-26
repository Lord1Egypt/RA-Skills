## Description: <br>
Automates verification that AI agents truly completed tasks by checking output files, system states, and logs for expected results and activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kgapol](https://clawhub.ai/user/kgapol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to verify agent deliverables before downstream work depends on them. It is suited for CI, cron, and operational checks that validate expected files, content markers, logs, and configured output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification paths or logs may include sensitive agent outputs. <br>
Mitigation: Keep check paths limited to intended agent output folders and review log contents before retaining or sharing them. <br>
Risk: Remote install snippets can obscure what is executed during setup. <br>
Mitigation: Install from the bundled files and review the shell scripts before running them. <br>
Risk: Optional AI quality checks may send file content to the configured Ollama or model runtime. <br>
Mitigation: Use --ai-check only for files that are appropriate for the configured local model workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kgapol/proof-of-work) <br>
- [Trust AI Stack on ClawMart](https://www.shopclawmart.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text reports] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled shell workflow can produce pass/fail text output, check logs, and generated reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
