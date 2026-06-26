## Description: <br>
Calls the Xiangyun API to perform structured passport OCR from local files or Base64 image input, extracting fields such as passport number, name, sex, birth date, issue date, expiry date, issuing authority, and nationality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liudengkui](https://clawhub.ai/user/liudengkui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit passport images to Xiangyun for structured OCR and to convert recognized passport fields into human-readable tables or export files. It is intended for workflows that need passport data extraction with explicit handling of API credentials and cached OCR results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passport images and extracted passport data are sent to the Xiangyun/netocr.com OCR service. <br>
Mitigation: Use the skill only when sending passport images to that service is acceptable for the user and use case. <br>
Risk: API credentials are stored in config.json and can be exposed through local files or command output. <br>
Mitigation: Treat config.json as a secret and avoid running credential-loading commands where output is logged. <br>
Risk: Recognized passport data may be cached locally and exported to JSON, CSV, or Excel files. <br>
Mitigation: Use --no-save unless cached results are needed and keep generated data files out of shared or synced folders. <br>


## Reference(s): <br>
- [Xiangyun Passport Recognition API Reference](references/api_docs.md) <br>
- [Xiangyun Product Page](https://www.netocr.com/products.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/liudengkui/ocr-passport-xiangyun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV, Excel files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON OCR results, table output, and optional CSV or Excel exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call an external Xiangyun OCR API, store API credentials in config.json, and cache recognized passport results next to source images unless --no-save is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
