## Description:

NanoGPT provider plugin for OpenClaw with dynamic model catalog, API-key authentication, and usage tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forceconstant](https://clawhub.ai/user/forceconstant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to configure NanoGPT as an OpenClaw model provider, discover current NanoGPT models, authenticate with API keys, and view usage or balance information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled final integration test can delete remote OpenClaw session data.

Mitigation: Run final_integration_test.sh only on disposable hosts or accounts, and review the target paths before execution.

Risk: API keys or session transcripts may be exposed through logs or collected test_results output.

Mitigation: Treat NanoGPT API keys as secrets, rotate any key that appears in logs, and keep test_results out of commits and shared artifacts.

Risk: The published package identity and dependency set should be verified before installation.

Mitigation: Confirm the exact package name, publisher, version, and dependencies before installing the plugin in a real OpenClaw environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/forceconstant/skills/nano-gpt-plugin)
- [NanoGPT API Introduction](https://docs.nano-gpt.com/introduction)
- [NanoGPT Authentication](https://docs.nano-gpt.com/authentication.md)
- [NanoGPT Models API](https://docs.nano-gpt.com/api-reference/endpoint/models.md)
- [NanoGPT Subscription Usage API](https://docs.nano-gpt.com/api-reference/endpoint/subscription-usage.md)
- [NanoGPT Check Balance API](https://docs.nano-gpt.com/api-reference/endpoint/check-balance.md)
- [OpenClaw Provider Plugin SDK](https://github.com/openclaw/openclaw/blob/main/docs/plugins/sdk-provider-plugins.md)

## Skill Output:

**Output Type(s):** [configuration, code, shell commands, guidance]

**Output Format:** [TypeScript plugin package with Markdown documentation and JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a NanoGPT API key for authenticated catalog, usage, and balance calls.]

## Skill Version(s):

0.1.3 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
