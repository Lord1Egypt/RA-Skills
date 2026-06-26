## Description: <br>
Translate text between Korean, English, Japanese, Chinese, and 10+ other languages using Naver Papago NMT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, localization teams, and agents use this skill to translate user-selected text or files through Naver Papago from command-line and Python workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, including content read from files, is sent to Naver Papago for translation. <br>
Mitigation: Avoid translating secrets, credentials, regulated data, or confidential material unless third-party processing by Naver is approved for the environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chloepark85/naver-papago-translate) <br>
- [ClawHub Metadata Homepage](https://github.com/ChloePark85/naver-papago-translate) <br>
- [Naver Developers](https://developers.naver.com/) <br>
- [Papago NMT API Reference](https://developers.naver.com/docs/papago/papago-nmt-api-reference.md) <br>
- [Papago NMT API Endpoint](https://openapi.naver.com/v1/papago/n2mt) <br>
- [Papago Language Detection Endpoint](https://openapi.naver.com/v1/papago/detectLangs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Plain text translation or JSON object with source, target, input_length, and translated fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Naver client ID and client secret; sends selected input text to Naver Papago over HTTPS.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, pyproject.toml, changelog, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
