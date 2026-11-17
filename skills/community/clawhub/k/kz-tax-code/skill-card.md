## Description:

Kazakhstan tax assistant that answers Russian and Kazakh questions about Kazakhstan tax-code articles, rates, deductions, benefits, KGD rules, and common declaration forms using bundled legal text and Node.js search scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k0zibek](https://clawhub.ai/user/k0zibek)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to retrieve grounded answers about Kazakhstan tax rules in Russian or Kazakh, including article lookups, tax rates, benefits, deductions, KGD rules, and common declaration forms. The skill is also used to search related official laws for annual indicators and contribution rates that are outside the tax code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a local legal-text helper and should not be treated as professional tax authority.

Mitigation: Verify important tax answers against official sources before acting on them.

Risk: Scripts can read from or write to local paths when arguments such as --file, --out, or --html are chosen by an untrusted prompt.

Mitigation: Keep file paths inside the skill data directory and do not let untrusted prompts choose file path arguments.

Risk: Automatic legal-data updates can use insecure downloads.

Mitigation: Prefer manually saved and verified HTML from adilet.zan.kz, and use insecure downloads only in trusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/k0zibek/skills/kz-tax-code)
- [Publisher profile](https://clawhub.ai/user/k0zibek)
- [Adilet legal document source](https://adilet.zan.kz)
- [Republican budget law metadata](https://adilet.zan.kz/rus/docs/Z2500000065)
- [Mandatory social medical insurance law metadata](https://adilet.zan.kz/rus/docs/Z1500000405)
- [Mandatory social insurance law metadata](https://adilet.zan.kz/rus/docs/Z2100000021)
- [Pension provision law metadata](https://adilet.zan.kz/rus/docs/Z1300000105)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and cited legal article references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should identify the tax-code version, article, and paragraph used; important tax answers require verification against official sources.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
