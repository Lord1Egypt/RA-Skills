## Description: <br>
Translates selected text fields in JSON files, especially description fields, while preserving the original JSON structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JEyeshield](https://clawhub.ai/user/JEyeshield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, localization teams, and data maintainers use this skill to translate selected JSON string fields into Chinese, English, Japanese, or Korean while keeping the file structure intact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected JSON field contents are sent to online translation services, which can expose sensitive, regulated, or confidential text. <br>
Mitigation: Use only on content approved for third-party translation services, and avoid secrets, private customer data, regulated data, and confidential configuration files. <br>
Risk: The translated JSON file is written to an output path chosen by the user or derived from the input filename. <br>
Mitigation: Verify the output path before running the skill and review the generated JSON before replacing any source file or relying on the translation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JEyeshield/json-translator) <br>
- [MyMemory translation API](https://api.mymemory.translated.net) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a translated UTF-8 JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a translated JSON file and prints progress, previews, missing-field warnings, and completion statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
