## Description: <br>
Multi-language license compliance audit powered by Trivy that detects GPL, AGPL, LGPL, MPL, BSL, and other risky licenses across common application stacks and can output terminal, Markdown, HTML, JSON, Feishu Doc, and Feishu Base reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theosunny](https://clawhub.ai/user/theosunny) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan local or remote repositories for dependency license risk before release, procurement review, or CI/CD enforcement. It is aimed at multi-language projects that need summarized license findings and optional team-review outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install Trivy by running a remote installer when Trivy is missing. <br>
Mitigation: Install and verify Trivy separately before running the skill, or run it only in an environment where that automatic installation behavior is acceptable. <br>
Risk: Private repository URLs may contain credentials if users pass tokens directly in the URL. <br>
Mitigation: Avoid embedding Git tokens in URLs; prefer credential helpers, scoped temporary credentials, or pre-cloned local repositories. <br>
Risk: NuGet enrichment and Feishu outputs can send dependency or report data to external services. <br>
Mitigation: Use --no-enrich for offline NuGet scans and enable Feishu output only for repositories whose dependency data may be uploaded to the configured Feishu account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theosunny/license-audit) <br>
- [Trivy](https://github.com/aquasecurity/trivy) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Code review checklist](references/code-review-checklist.md) <br>
- [Known license table](references/known-licenses.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown, HTML, JSON, Feishu Doc, or Feishu Base records depending on selected options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports classify license findings by risk tier and may include NuGet enrichment for C#/.NET projects.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
