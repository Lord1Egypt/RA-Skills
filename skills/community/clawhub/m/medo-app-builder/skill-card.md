## Description: <br>
Create, modify, generate, and deploy websites, web apps, dashboards, SaaS products, internal tools, interactive web pages, Weixin mini programs, and games on the Baidu Medo platform using natural-language instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seiriosplus](https://clawhub.ai/user/seiriosplus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to create, iterate on, generate, and publish Medo web apps from natural-language requests through the packaged CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Medo API key to create, modify, inspect, generate, and publish applications in the user's Medo account. <br>
Mitigation: Use a revocable least-privilege API key, avoid committing the key to files, and review account access before installation. <br>
Risk: Generation or publishing can produce publicly accessible applications without a clearly required final user confirmation step. <br>
Mitigation: Instruct the agent to ask before running generate-app or publish, inspect the app before publication, and use publish status checks to verify the result. <br>
Risk: Using an unexpected Medo API endpoint could send application prompts or account actions to the wrong service. <br>
Mitigation: Verify the default API endpoint with Medo before use and avoid overriding it unless the alternate endpoint is trusted. <br>


## Reference(s): <br>
- [Medo Official Website](https://www.medo.dev) <br>
- [ClawHub Skill Page](https://clawhub.ai/seiriosplus/medo-app-builder) <br>
- [Publisher Profile](https://clawhub.ai/user/seiriosplus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or URL command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MEDO_API_KEY; command results may include app identifiers, conversation identifiers, deployment status, and production URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
