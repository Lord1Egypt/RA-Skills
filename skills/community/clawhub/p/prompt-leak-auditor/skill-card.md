## Description: <br>
Audits prompts, skill files, and documentation for leaked secrets, internal paths, internal rules, or high-risk instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt authors, and security reviewers use this skill to audit prompts, SKILL.md files, README files, or directories before release and produce masked, reviewable remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auditing broad directories can expose more sensitive prompt, URL, command, or configuration text than intended. <br>
Mitigation: Run the skill only on files or directories selected for audit, preferably a copied prompt, SKILL.md, README, or small repository subset. <br>
Risk: Generated reports may include non-secret internal snippets that should not be shared widely. <br>
Mitigation: Review the Markdown output before sharing and redact any internal URLs, command text, or other sensitive context that remains. <br>
Risk: Detected secrets or high-sensitivity content could be redistributed if copied verbatim into follow-up messages. <br>
Mitigation: Keep high-sensitivity findings masked by default and use the report for remediation planning rather than reposting the original values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/prompt-leak-auditor) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports or JSON, with optional local shell command invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports default to masking high-sensitivity content; the local script supports input and output paths, markdown/json format, result limits, and dry-run mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
