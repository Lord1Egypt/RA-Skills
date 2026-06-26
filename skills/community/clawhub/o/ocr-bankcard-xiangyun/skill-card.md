## Description: <br>
Calls the Xiangyun Bank Card Recognition API (typeId=17) to extract card number, card type, card name, issuing bank, and bank code from bank card images supplied as local files or Base64. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liudengkui](https://clawhub.ai/user/liudengkui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run bank card OCR through Xiangyun/netocr.com, configure API credentials, review structured recognition results, and export cached results when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank card images, OCR results, cached JSON files, CSV or Excel exports, terminal output, and config.json can contain sensitive card data or API credentials. <br>
Mitigation: Process only images with appropriate consent and compliance review, treat generated files and logs as sensitive, prefer --no-save when persistence is unnecessary, delete cached results after use, and avoid sharing config files or output containing secrets. <br>
Risk: The skill sends bank card images and OCR credentials to Xiangyun/netocr.com for recognition. <br>
Mitigation: Install and use the skill only when that external processing is acceptable for the intended data, jurisdiction, and organization policy. <br>


## Reference(s): <br>
- [Xiangyun Bank Card Recognition API Documentation](references/api_docs.md) <br>
- [Xiangyun Bank Card OCR Product Page](https://www.netocr.com/bankCard.html) <br>
- [Xiangyun Platform](https://www.netocr.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/liudengkui/ocr-bankcard-xiangyun) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON OCR results, human-readable tables, and optional CSV, Excel, or JSON export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recognition results may be cached as JSON beside source images unless --no-save is used; exports are generated only on explicit request.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
