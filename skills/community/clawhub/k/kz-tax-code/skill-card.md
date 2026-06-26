## Description: <br>
Kazakhstan Tax Assistant helps agents answer Kazakhstan tax questions in Russian and Kazakh by searching bundled Tax Code texts and related law references for articles, rates, deductions, benefits, declaration forms, and tax calculation rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k0zibek](https://clawhub.ai/user/k0zibek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, employees, and agents use this skill to look up Kazakhstan tax-law provisions, cite the relevant Tax Code version and article, and support bilingual tax explanations or calculations grounded in bundled legal texts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node.js scripts that can search bundled legal texts and optionally fetch or update law files. <br>
Mitigation: Run the scripts in an intended workspace and review commands before execution. <br>
Risk: The documented --insecure option disables TLS certificate verification for automatic downloads. <br>
Mitigation: Prefer manual HTML download; use --insecure only on a trusted network. <br>
Risk: The --file option can point searches at local files outside the intended law-document set. <br>
Mitigation: Keep --file paths limited to intended Kazakhstan law documents. <br>
Risk: Tax rates and thresholds change over time, and stale values could produce misleading guidance. <br>
Mitigation: Use the bundled source metadata and primary legal texts, and clearly mark knownValues as requiring verification when fresh downloads are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/k0zibek/kz-tax-code) <br>
- [Publisher profile](https://clawhub.ai/user/k0zibek) <br>
- [Bundled law metadata](artifact/data/laws.json) <br>
- [Bundled Tax Code version metadata](artifact/data/versions.json) <br>
- [Republican budget law, Russian](https://adilet.zan.kz/rus/docs/Z2500000065) <br>
- [Republican budget law, Kazakh](https://adilet.zan.kz/kaz/docs/Z2500000065) <br>
- [Mandatory social medical insurance law, Russian](https://adilet.zan.kz/rus/docs/Z1500000405) <br>
- [Mandatory social medical insurance law, Kazakh](https://adilet.zan.kz/kaz/docs/Z1500000405) <br>
- [Pension provision law, Russian](https://adilet.zan.kz/rus/docs/Z1300000105) <br>
- [Pension provision law, Kazakh](https://adilet.zan.kz/kaz/docs/Z1300000105) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown answers with legal citations and optional inline shell commands for local search or document updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Russian and Kazakh output; uses local Node.js scripts for search, optional fetching, and updates.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
