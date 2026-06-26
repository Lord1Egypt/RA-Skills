## Description: <br>
Phy I18n Audit audits multi-locale codebases by diffing locale files against a base locale to identify missing, untranslated, empty, and orphaned translation keys, then reports coverage and CI fail-gate guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and localization engineers use this skill to audit i18n key coverage across JSON, YAML, PO/POT, and ARB locale files before release and to prepare translation follow-up or CI gating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit requires the agent to read locale files and basic project metadata in the repository where it runs. <br>
Mitigation: Run it only in intended repositories and review the reported file scope before relying on results. <br>
Risk: Generated scaffold files or suggested CI commands may introduce incorrect changes or unreviewed package execution, especially the optional npx command. <br>
Mitigation: Review generated files and commands before committing or running them, and pin or approve any CI dependency before adoption. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-i18n-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with tables, code blocks, shell commands, and optional JSON scaffold examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pure local file analysis; optional scaffold files and CI commands should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
