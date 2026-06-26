## Description: <br>
Translate text and images between multiple languages using Xiangji and supported translation engines such as Baidu, Google, DeepL, and ChatGPT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcdentoncore](https://clawhub.ai/user/jcdentoncore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to translate individual or batch text and image inputs through Xiangji/tosoiot translation APIs, including local image files and image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text, image files, image URLs, and service keys are sent to Xiangji/tosoiot translation APIs. <br>
Mitigation: Use only provider-approved content and credentials; avoid confidential, regulated, internal-only, or secret-bearing inputs unless the provider is approved for that use case. <br>
Risk: Examples pass API keys and signing keys on command lines, which can expose secrets through shell history or process listings. <br>
Mitigation: Prefer safer local key handling such as environment variables, secret managers, or short-lived credentials when adapting the commands. <br>


## Reference(s): <br>
- [Xiangji Translation Service](https://www.xiangjifanyi.com/) <br>
- [Xiangji API Documentation](https://openapi-doc.xiangjifanyi.com/) <br>
- [Xiangji Console](https://www.xiangjifanyi.com/console/workspace) <br>
- [Supported Languages](references/languages.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Xiangji/tosoiot API credentials and sends selected text, image files, or image URLs to third-party translation APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
