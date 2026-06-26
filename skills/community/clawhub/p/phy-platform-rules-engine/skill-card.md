## Description: <br>
Checks draft social-media posts for platform-specific rule issues and returns PASS/WARN/FAIL feedback with fix suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and developers use this skill to pre-check Reddit, LinkedIn, Twitter/X, and Hacker News drafts before publishing. It returns rule-level feedback and suggested edits, but its platform-ranking advice should be treated as advisory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft content may contain secrets, personal data, or embargoed material. <br>
Mitigation: Only analyze content the user is authorized to process, and avoid entering sensitive information unless that handling is approved. <br>
Risk: Platform-ranking guidance may be incomplete or change after release. <br>
Mitigation: Treat recommendations as advisory pre-flight feedback and review final posts against current platform policies before publishing. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-platform-rules-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, shell commands] <br>
**Output Format:** [Plain-text report or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit code 0 for clear results, 1 for warnings, and 2 for failures.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
