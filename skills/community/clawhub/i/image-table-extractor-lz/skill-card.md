## Description: <br>
Extracts table data from uploaded images and returns the results as Markdown tables and CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuzheng60](https://clawhub.ai/user/liuzheng60) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract visible tabular data from experiment or data-table images, preserve headers and cell values, filter pass/通过 markers, and return matched Markdown and CSV outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images may be sent to a third-party OCR provider without clear disclosure of retention, consent, or data handling terms. <br>
Mitigation: Use only non-confidential images unless the provider, retention policy, consent flow, and data handling terms are documented and acceptable. <br>
Risk: The skill requires the KETOP_KEY_TOKEN credential for the fallback image parsing workflow. <br>
Mitigation: Treat the API key as a secret, provide it through a temporary environment variable, and avoid pasting it into chat or storing it in shell profiles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuzheng60/image-table-extractor-lz) <br>
- [Publisher profile](https://clawhub.ai/user/liuzheng60) <br>
- [CSV format reference](references/csv-format.md) <br>
- [Image table extraction reference](references/img-table.md) <br>
- [Ketop image table API endpoint](https://kpp.ketop.cn/Api/KpAiImgTbApi?act=imgtb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown table plus CSV code block, with optional shell command guidance for image parsing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill aims to keep extracted data consistent across Markdown and CSV outputs while preserving visible headers and cell values.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
