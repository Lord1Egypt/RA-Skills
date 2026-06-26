## Description: <br>
OpenNotebook knowledge management platform client for notebooks, sources, notes, AI search, transformation pipelines, models, embeddings, chat, podcasts, and related API operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iazrael](https://clawhub.ai/user/iazrael) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate an OpenNotebook knowledge management server from the command line or Python, including notebook management, source ingestion, note management, search, transformations, and model operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload private files and text to the configured OpenNotebook server. <br>
Mitigation: Verify the server base URL and require explicit approval before uploading sensitive content. <br>
Risk: The skill can delete notebooks, sources, and notes or administer server resources. <br>
Mitigation: Review destructive commands before execution and use least-privilege API credentials where possible. <br>
Risk: API keys are required for protected endpoints. <br>
Mitigation: Store OPENNOTEBOOK_API_KEY securely, avoid exposing it in logs or tests, and do not run integration tests with real secrets unless intentionally authorized. <br>


## Reference(s): <br>
- [OpenNotebook API Reference](artifact/api_reference.md) <br>
- [ClawHub OpenNotebook Release](https://clawhub.ai/iazrael/opennotebook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python code examples, and JSON API responses from the configured OpenNotebook server] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus OPENNOTEBOOK_BASE_URL and OPENNOTEBOOK_API_KEY configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
