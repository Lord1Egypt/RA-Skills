## Description: <br>
Security vetting protocol before installing any AI agent skill. Red flag detection for credential theft, obfuscated code, exfiltration. Risk classification LOW/MEDIUM/HIGH/EXTREME. Produces structured vetting reports. Never install untrusted skills without running this first. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiyi-9](https://clawhub.ai/user/yiyi-9) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill before installing or running unknown skills to inspect source, permissions, and security red flags, then produce a structured vetting report with a risk level and recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advisory and does not sandbox, block, or enforce execution of reviewed artifacts. <br>
Mitigation: Inspect downloaded files without executing them, review the generated vetting report, and decide separately whether installation is acceptable. <br>
Risk: Publisher or source trust may be unclear because server-resolved GitHub import provenance is unavailable for this version. <br>
Mitigation: Verify the ClawHub listing and publisher profile before relying on provenance-sensitive conclusions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yiyi-9/openclaw-skill-vetter-1-0-0) <br>
- [Skill Homepage](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with checklists, risk classifications, vetting report templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory review output; it does not sandbox or enforce installation decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
