## Description: <br>
Access dynamic NanoGPT models in OpenClaw with API key authentication, usage tracking, balance checks, and support for multiple model families. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forceconstant](https://clawhub.ai/user/forceconstant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to route agent model calls through NanoGPT, discover available models, onboard a NanoGPT API key, and monitor usage or account balance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model calls use the user's NanoGPT API key and may consume NanoGPT credits. <br>
Mitigation: Install only when NanoGPT access is intended, treat the API key like a password, and monitor usage and balance through the plugin or NanoGPT account tools. <br>
Risk: The included final integration test deletes remote OpenClaw plugin and session data and passes the API key over an SSH command line. <br>
Mitigation: Run final_integration_test.sh only in a disposable test environment and avoid exposing API keys through shell history or shared terminals. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/forceconstant/nano-gpt-plugin) <br>
- [NanoGPT API introduction](https://docs.nano-gpt.com/introduction) <br>
- [NanoGPT authentication](https://docs.nano-gpt.com/authentication.md) <br>
- [NanoGPT models API](https://docs.nano-gpt.com/api-reference/endpoint/models.md) <br>
- [NanoGPT subscription usage API](https://docs.nano-gpt.com/api-reference/endpoint/subscription-usage.md) <br>
- [NanoGPT balance API](https://docs.nano-gpt.com/api-reference/endpoint/check-balance.md) <br>
- [NanoGPT OpenClaw integration](https://docs.nano-gpt.com/integrations/openclaw.md) <br>
- [OpenClaw provider plugin SDK](https://github.com/openclaw/openclaw/blob/main/docs/plugins/sdk-provider-plugins.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [OpenAI-compatible chat completions returned through OpenClaw model responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected NanoGPT-hosted model and the user's NanoGPT account, credits, and API key configuration.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
