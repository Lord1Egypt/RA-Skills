## Description: <br>
Complete Windows setup guide for Ollama: installation, CORS header fix for web apps, custom model creation with Modelfiles, and integration with desktop AI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and local AI users use this skill to set up Ollama on Windows, configure browser access, create custom Modelfile-based models, and troubleshoot common runtime issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide recommends setting OLLAMA_ORIGINS=* permanently, which allows browser requests from any origin. <br>
Mitigation: Prefer setting OLLAMA_ORIGINS only to exact trusted app origins, such as a specific localhost port, and reserve wildcard origins for controlled temporary tests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TheShadowRose/ollama-windows-guide) <br>
- [Ollama](https://ollama.com) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline PowerShell, bash, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; commands and environment changes should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
