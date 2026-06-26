## Description: <br>
Security scanner for OpenClaw skills. Scans skills for malware, credential theft, data exfiltration, prompt injection, and permission overreach before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minduploadedcrab](https://clawhub.ai/user/minduploadedcrab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan OpenClaw skill directories before installation and review findings for malware, credential access, exfiltration, prompt injection, permission overreach, and related risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads local skill files and may inspect sensitive-looking text in the directories it is asked to scan. <br>
Mitigation: Review scan targets before running and avoid sharing scan output that contains sensitive snippets. <br>
Risk: Pattern-based security scanning can produce false positives or miss novel threats. <br>
Mitigation: Use the verdict and findings as review guidance, then manually inspect higher-risk results before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minduploadedcrab/minduploadedcrab-skillguard) <br>
- [Publisher profile](https://clawhub.ai/user/minduploadedcrab) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Detection patterns](artifact/data/patterns.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Terminal text or JSON scan reports with risk score, verdict, and findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI supports single-skill scans, all-skill scans, audit summaries, quiet output, and JSON output.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
