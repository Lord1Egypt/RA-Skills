## Description: <br>
Photo Index With LLM scans selected photo folders, analyzes images with local or explicitly configured remote vision-language models, stores a local SQLite index, and supports natural-language photo search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to scan personal or work photo directories, build searchable local indexes, and retrieve matching photos from natural-language queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote model analysis can send full images to the configured provider. <br>
Mitigation: Use local-only mode for sensitive photos and enable remote analysis only after reviewing the provider and consent settings. <br>
Risk: The local database and .env file can contain sensitive paths, image-derived metadata, or credentials. <br>
Mitigation: Restrict file permissions, avoid committing local data files, and protect the SQLite database and .env file. <br>
Risk: Search output can expose local photo paths and descriptive metadata. <br>
Mitigation: Run the skill only in trusted environments and review outputs before sharing them outside the local workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-photo-index) <br>
- [Privacy guide](artifact/PRIVACY_GUIDE.md) <br>
- [Cross-platform support](artifact/CROSS_PLATFORM.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text or JSON from CLI commands, with Markdown documentation examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results and statistics may include local photo paths, tags, descriptions, confidence scores, and model connection status.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
