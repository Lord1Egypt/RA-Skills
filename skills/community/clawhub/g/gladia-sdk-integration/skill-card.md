## Description: <br>
Install and configure the official Gladia SDKs (@gladiaio/sdk for JS/TS, gladiaio-sdk for Python). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gladiaio](https://clawhub.ai/user/gladiaio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up Gladia SDK clients, configure API keys and regions, choose JavaScript/TypeScript or Python usage patterns, and decide when SDK usage is preferable to raw API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples that upload files or stream microphone input send audio to Gladia's service. <br>
Mitigation: Tell users to get appropriate consent, handle audio according to their privacy requirements, and disclose service-side processing before uploading or streaming. <br>
Risk: API keys can be exposed if copied into browser-side code. <br>
Mitigation: Keep API keys server-side where possible and use a backend proxy for browser integrations. <br>
Risk: Delete methods can remove jobs, sessions, transcripts, or associated audio. <br>
Mitigation: Require clear user confirmation before generating or running delete operations. <br>


## Reference(s): <br>
- [SDK integration guide](https://docs.gladia.io/chapters/integrations/sdk) <br>
- [JavaScript SDK on npm](https://www.npmjs.com/package/@gladiaio/sdk) <br>
- [Python SDK on PyPI](https://pypi.org/project/gladiaio-sdk/) <br>
- [SDK source code](https://github.com/gladiaio/sdk) <br>
- [Code samples](https://github.com/gladiaio/gladia-samples) <br>
- [Current SDK versions](./references/sdk-versions.md) <br>
- [Client configuration reference](./references/client-config.md) <br>
- [JavaScript and TypeScript SDK patterns](./references/javascript.md) <br>
- [Python SDK patterns](./references/python.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SDK installation commands, client configuration snippets, and integration guidance for Gladia API usage.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
