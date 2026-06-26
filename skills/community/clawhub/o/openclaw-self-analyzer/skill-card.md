## Description: <br>
Analyzes OpenClaw architecture, detects hook points, generates hook code, scans code, and produces architecture reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fofo365](https://clawhub.ai/user/fofo365) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a local OpenClaw installation, map pipeline stages and hook points, generate starter hooks, and create Markdown or JSON reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated hooks may log sensitive conversation, prompt, or memory context. <br>
Mitigation: Review generated hook files before enabling them and remove or narrow full-context console logging, especially around prompt, LLM submission, and memory stages. <br>
Risk: Architecture reports are heuristic and may misidentify pipeline details. <br>
Mitigation: Validate generated reports against the local OpenClaw installation before using them to configure hooks or extensions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fofo365/openclaw-self-analyzer) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Architecture Report](artifact/reports/architecture_report.md) <br>
- [Generated Hook Manifest](artifact/generated_hooks/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, JavaScript hook code, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local architecture reports and hook files for review before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
