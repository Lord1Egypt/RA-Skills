## Description: <br>
Monitors local OpenClaw version daily at 06:00 Beijing time against NVD and GitHub advisories, reporting found CVEs with remediation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronjager92](https://clawhub.ai/user/aaronjager92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check an OpenClaw installation against NVD CVE data and GitHub Security Advisories, then receive remediation-oriented output when matching vulnerabilities are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an enabled daily OpenClaw cron job. <br>
Mitigation: Review setup_cron.sh before installation and confirm how to disable or remove the openclaw-self-guard job. <br>
Risk: The vulnerability check can falsely report no vulnerabilities when data-source checks fail. <br>
Mitigation: Do not rely on the results until helper argument parsing and fail-open no-vulnerability behavior are fixed; confirm important findings against NVD and GitHub advisories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaronjager92/openclaw-self-guard) <br>
- [NVD CVE API](https://services.nvd.nist.gov/rest/json/cves/2.0) <br>
- [GitHub Security Advisories API](https://api.github.com/advisories) <br>
- [requirements.txt](references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report or JSON status with vulnerability counts, local version, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run silently when no vulnerabilities are detected; the cron setup installs an enabled daily OpenClaw job.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
