## Description: <br>
Internationalization and localization readiness scanner that detects hardcoded strings, missing translations, locale-sensitive formatting, RTL issues, string concatenation in translations, and i18n anti-patterns across supported codebases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use i18ncheck to scan applications for localization readiness issues, generate audit reports, and optionally install pre-commit checks that block new high-severity i18n regressions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook installation and baseline commands can modify repository files. <br>
Mitigation: Run these commands deliberately and review generated lefthook.yml and .i18ncheck-baseline.json files before committing them. <br>
Risk: License keys are sensitive credentials. <br>
Mitigation: Store I18NCHECK_LICENSE_KEY privately and avoid committing it to source control or shared logs. <br>
Risk: Allowlists and baselines can hide known findings from later scan output. <br>
Mitigation: Review allowlist and baseline entries periodically so suppressed issues remain intentional and tracked. <br>


## Reference(s): <br>
- [ClawHub i18ncheck listing](https://clawhub.ai/suhteevah/i18ncheck) <br>
- [I18nCheck website](https://i18ncheck.pages.dev) <br>
- [artifact/README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text, Markdown reports, shell command results, and repository configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan findings include file paths, line numbers, check IDs, severities, descriptions, recommendations, and readiness scores.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
