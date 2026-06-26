## Description: <br>
Looper helps agents configure and manage scheduled automation loops for content generation, code review, blog publishing, and social media posting through looper.bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Builder-NC](https://clawhub.ai/user/Builder-NC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and social media teams use Looper to create and manage scheduled AI automation loops for repositories, blogs, and social channels. The skill is useful when an agent needs API-based setup, monitoring, or control of recurring Looper workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Looper can create persistent workflows that change GitHub repositories, publish social posts, manage API keys, and run with broad delegated authority. <br>
Mitigation: Prefer propose or notify mode, set explicit run limits, confirm create/update/delete/run actions, and review the first run before enabling unattended operation. <br>
Risk: Credentials and third-party API keys may be exposed through prompts, environment variables, or social posting configuration. <br>
Mitigation: Keep LOOPER_ADMIN_KEY and posting keys out of prompts where possible, store them as secrets, and rotate any exposed keys. <br>
Risk: Automated generated content or code changes may be incorrect or misleading. <br>
Mitigation: Review generated content, pull requests, and run output before publishing or merging. <br>


## Reference(s): <br>
- [Looper](https://looper.bot) <br>
- [Looper API](https://api.looper.bot) <br>
- [Looper API Reference](references/api-reference.md) <br>
- [Looper source](https://github.com/dbhurley/looper) <br>
- [ClawHub skill page](https://clawhub.ai/Builder-NC/looper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or manage persistent scheduled Looper workflows through authenticated API calls.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
