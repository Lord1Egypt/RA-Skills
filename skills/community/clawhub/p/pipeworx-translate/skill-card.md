## Description: <br>
Translate text between multiple languages, detect text language, and list supported language codes and names through the Pipeworx translation gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add machine translation, language detection, and supported-language lookup to an MCP-capable client or workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for translation is sent to an external Pipeworx/LibreTranslate endpoint. <br>
Mitigation: Do not submit secrets, credentials, regulated data, or private business content unless the provider's data-handling practices have been reviewed and accepted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-translate) <br>
- [Pipeworx translation MCP endpoint](https://gateway.pipeworx.io/translate/mcp) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Text or Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Translation and detection results are returned by the external Pipeworx/LibreTranslate endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
