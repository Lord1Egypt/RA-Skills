## Description: <br>
Open source license compliance scanner that catches copyleft, viral, and problematic licenses in dependencies before they create legal risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering teams, and compliance reviewers use LicenseGuard to scan local dependency manifests for license risk, generate compliance reports or SBOMs, and optionally enforce approved-license policies through git hooks or CI checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/suhteevah/licenseguard) <br>
- [LicenseGuard website](https://licenseguard.pages.dev) <br>
- [LicenseGuard pricing](https://licenseguard.pages.dev/#pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text, markdown reports, JSON SBOM output, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scans read project dependency files; review lefthook configuration before installing hooks because it changes commit behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
