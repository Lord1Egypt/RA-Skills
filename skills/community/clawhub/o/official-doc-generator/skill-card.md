## Description: <br>
Generates and formats formal official documents such as meeting minutes, speeches, discussion outlines, and work reports using GB/T 9704-2012-style formatting, official-language style guidance, template tooling, sensitive-word checks, and local Python document-processing scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leaproud](https://clawhub.ai/user/leaproud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document authors use this skill to generate, format, validate, and revise formal official or organizational documents in Word-compatible formats. It is intended for workflows that need standardized layout, official-language phrasing, sensitive-word checks, and local revision tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local document generation and revision-history files can contain confidential official or business content. <br>
Mitigation: Use a controlled output folder, disable enhanced revision history with --no-history when appropriate, and review generated data, history, and template files before sharing or archiving the workspace. <br>
Risk: The skill runs local Python document-processing scripts and dependencies that write files and manage templates. <br>
Mitigation: Install and run it only in an environment where local Python scripts and document-processing dependencies are acceptable, and review templates and configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leaproud/official-doc-generator) <br>
- [GB/T 9704-2012 formatting reference](artifact/references/gb_t_9704_2012_standard.md) <br>
- [Official language style guide](artifact/references/official_language_style.md) <br>
- [Document type specification](artifact/references/document_types_specification.md) <br>
- [Sensitive words and checking rules](artifact/references/sensitive_words_list.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance, JSON configuration, Python command examples, and generated Word-compatible document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local output documents, revision-history files, templates, and validation reports in user-selected directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata; artifact _meta.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
