## Description: <br>
Giraffe Guard scans OpenClaw skill directories for supply chain attack patterns, malicious code, and suspicious behavior with context-aware detection and report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lida408](https://clawhub.ai/user/lida408) <br>

### License/Terms of Use: <br>
Apache License 2.0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan OpenClaw skills before installation or during CI/CD checks, helping identify critical and warning-level supply chain risks before enabling a skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include private source lines, secrets, or credential-like strings from scanned content. <br>
Mitigation: Treat reports as sensitive artifacts, store them only in trusted locations, and redact findings before sharing outside the intended review group. <br>
Risk: The scanner is intended to inspect local directories or repositories selected by the user, so scanning untrusted or unintended paths can expose irrelevant or sensitive files in findings. <br>
Mitigation: Run it only on directories or repositories intended for review, and use skip-directory and whitelist options to keep scans scoped. <br>
Risk: Detection results can require human judgment because security scanners may report patterns that are legitimate in context. <br>
Mitigation: Review warnings and critical findings before acting, and document approved exceptions in a whitelist file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lida408/giraffe-guard) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lida408) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, SARIF, Shell commands, Guidance] <br>
**Output Format:** [Terminal text, JSON reports, SARIF reports, and Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes distinguish clean scans, warnings, and critical findings; optional verbose context, quiet mode, severity thresholds, skipped rules, skipped directories, and whitelist files affect report detail.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata and scripts/audit.sh VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
