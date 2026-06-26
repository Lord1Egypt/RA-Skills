## Description: <br>
Enterprise AI security scanner combining static code analysis, runtime guards, ClamAV integration, and tamper-evident audit logging to detect threats in AI agent code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan AI agent code, review suspicious behavior, and configure runtime protection or audit reporting before deploying agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may invoke the skill during ordinary security-related discussion. <br>
Mitigation: Install it only when security scanning or code-audit assistance is intended, and narrow activation wording before broader deployment. <br>
Risk: Scanner results can miss unknown patterns or produce false positives from detection signatures. <br>
Mitigation: Treat reports as review input, confirm findings manually, and audit code before deployment. <br>


## Reference(s): <br>
- [OpenClaw Shield repository linked in skill documentation](https://github.com/pfaria32/OpenClaw-Shield-Security) <br>
- [Resonant source attribution](https://github.com/ManoloRemiddi/resonantos-open-system-toolkit/blob/main/BUILD_YOUR_OWN_SHIELD.md) <br>
- [ClawHub skill page](https://clawhub.ai/kenswj/openclaw-shield-1-0-3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON report references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide users to produce JSON scan reports and configure allowlists or audit logging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
