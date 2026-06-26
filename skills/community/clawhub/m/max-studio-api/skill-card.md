## Description: <br>
Integrate with the Max Studio API for image and video generation, uploads, task polling, media downloads, and batch result packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[voidreal](https://clawhub.ai/user/voidreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external integrators use this skill to work with Max Studio image and video generation APIs, including task creation, status polling, media upload flows, and signed URL downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided API keys, Google access tokens, prompts, and media URLs to the Max Studio service. <br>
Mitigation: Use only tokens intended for Max Studio, prefer short-lived tokens, and avoid placing secrets in chat logs or shell history. <br>
Risk: Private or secret-bearing media URLs submitted to the service or download command may expose sensitive assets. <br>
Mitigation: Submit only media URLs that are safe to share with Max Studio and choose download paths deliberately. <br>


## Reference(s): <br>
- [API Integration Guide - Max Studio](references/api_docs.md) <br>
- [Max Studio API endpoint](https://max-studio.store) <br>
- [Max Studio account registration](https://max-studio.shop) <br>
- [ClawHub skill page](https://clawhub.ai/voidreal/max-studio-api) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/voidreal) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON API responses, and downloaded files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Max Studio API keys and, for most media endpoints, a Google access token.] <br>

## Skill Version(s): <br>
1.0.7 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
