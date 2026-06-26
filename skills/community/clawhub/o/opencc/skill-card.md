## Description: <br>
OpenCC converts Chinese text between Simplified, Traditional, Taiwan, Hong Kong, and Japanese Kanji variants with phrase-level and regional terminology support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai-tw](https://clawhub.ai/user/kai-tw) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, writers, and localization workflows use this skill to convert Chinese text across Simplified, Traditional, Taiwan, Hong Kong, and Japanese Kanji variants while preserving regional terminology. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the OpenCC dependency from an untrusted package source could introduce supply-chain risk. <br>
Mitigation: Install dependencies from a trusted package source and pin or review dependency versions according to the deployment environment. <br>
Risk: A user-specified output path could overwrite an important file. <br>
Mitigation: Choose output paths deliberately and review paths before running file-writing conversions. <br>
Risk: Converted text may be inappropriate for proper nouns, technical terms, or region-specific wording. <br>
Mitigation: Review converted text when accuracy matters, especially for names, brand terms, and regional terminology. <br>


## Reference(s): <br>
- [OpenCC Conversion Modes Guide](references/opencc_guide.md) <br>
- [OpenCC Documentation](https://byvoid.github.io/OpenCC/) <br>
- [OpenCC GitHub](https://github.com/BYVoid/OpenCC) <br>
- [ClawHub OpenCC Skill](https://clawhub.ai/kai-tw/opencc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Guidance, Files] <br>
**Output Format:** [Plain text conversion output with Markdown guidance and Python or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read UTF-8 text from arguments, stdin, or an input file and write converted text to stdout or a user-specified output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
