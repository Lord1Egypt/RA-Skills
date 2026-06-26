## Description: <br>
OneDrive Photo Batch helps agents filter, index, OCR, semantically search, move, upload, delete, restore, and export OneDrive photo collections while keeping temporary downloads short-lived. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanqeur](https://clawhub.ai/user/lanqeur) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal productivity users use this skill to manage OneDrive photo libraries through filtered search, OCR and multimodal indexing, semantic lookup, export, and controlled write operations. It is intended for agents that can prepare configuration, run the bundled Python runtime, and review JSON or file outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change OneDrive photos, including delete, restore, move, and upload operations when write mode is enabled. <br>
Mitigation: Keep mode.read_only=true for inspection and indexing, use Files.Read scopes where possible, and enable write actions only with narrow filters, limits, and explicit user confirmation. <br>
Risk: The runtime can reuse cached Microsoft credentials from the configured token cache path. <br>
Mitigation: Store the token cache in a protected workspace path, verify the Microsoft account before running, and revoke or rotate access if the cache is exposed. <br>
Risk: Selected photos, OCR text, summaries, or embeddings may be sent to the configured OCR and embedding providers. <br>
Mitigation: Use approved provider endpoints and API keys, disable embeddings or external OCR for sensitive albums, and avoid processing confidential photo sets without review. <br>


## Reference(s): <br>
- [OneDrive Photo Batch ClawHub Release](https://clawhub.ai/lanqeur/onedrive-photo-batch) <br>
- [Configuration Template](artifact/references/config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV files] <br>
**Output Format:** [Markdown guidance with bash commands; runtime commands return JSON status and can export JSON or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a JSON configuration file, local token cache, SQLite index, temporary download directory, and optional local recycle directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
