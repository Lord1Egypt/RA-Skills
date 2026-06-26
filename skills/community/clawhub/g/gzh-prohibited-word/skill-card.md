## Description: <br>
扫描公众号文案、文件或网页中的违禁词与敏感表述，标注风险并提供合规替换建议，帮你安全过审、避免删文限流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WeChat Official Account operators, new media editors, brand teams, and designers use this skill to check draft copy, uploaded text files, extracted page text, or image text for prohibited wording before publication. The skill returns highlighted risks, replacement guidance, and an optimized copy file for review and reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says checked copy, extracted file text, and fetched webpage text are sent to RedFoxHub for analysis. <br>
Mitigation: Use only with content approved for that external data flow, and avoid submitting confidential or regulated material unless the organization has approved the service. <br>
Risk: The security scan notes that the skill scans shell startup files for REDFOX_API_KEY. <br>
Mitigation: Prefer a dedicated environment or secret mechanism for REDFOX_API_KEY, and avoid storing the key in shell startup files. <br>
Risk: The security scan notes that optimized copy is written to a local text file after detection. <br>
Mitigation: Review generated files before sharing or committing them, and remove local outputs that contain sensitive source copy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/gzh-prohibited-word) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [Core workflow](artifact/references/core_workflow.md) <br>
- [Detection script](artifact/scripts/check_sensitive_words.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown detection results and replacement tables, plus a plain-text optimized copy file; the helper script emits JSON for the agent to parse.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends checked content, extracted file text, or fetched webpage text to RedFoxHub for analysis.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
