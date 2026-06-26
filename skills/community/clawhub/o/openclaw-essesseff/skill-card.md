## Description: <br>
Interact with the essesseff DevOps platform to call its public API, manage app lifecycle operations, promote images across environments, configure Argo CD, and use the essesseff onboarding utility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamdurst](https://clawhub.ai/user/adamdurst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to manage essesseff apps, deployments, image promotion, Argo CD setup, retention policies, and package cleanup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide production deployments and app lifecycle changes. <br>
Mitigation: Require explicit human approval before PROD deployments and other environment promotion actions. <br>
Risk: The skill can guide repository creation, package deletion, and repository visibility changes. <br>
Mitigation: Use least-privilege credentials, prefer short-lived tokens, and require human approval before destructive or visibility-changing operations. <br>
Risk: The skill uses API keys, GitHub PATs, .essesseff files, and notifications-secret.yaml. <br>
Mitigation: Keep secrets out of Git, logs, prompts, and shared transcripts, and delete temporary secret files after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adamdurst/openclaw-essesseff) <br>
- [essesseff onboarding utility](https://github.com/essesseff/essesseff-onboarding-utility) <br>
- [essesseff platform](https://www.essesseff.com) <br>
- [essesseff Public API overview](references/api-overview.md) <br>
- [Apps API](references/api-apps.md) <br>
- [Environments API](references/api-environments.md) <br>
- [Images API](references/api-images.md) <br>
- [Packages API](references/api-packages.md) <br>
- [Retention Policies API](references/api-retention-policies.md) <br>
- [Onboarding Utility](references/onboarding-utility.md) <br>
- [Prerequisites Reference](references/prerequisites.md) <br>
- [Non-Subscriber Mode Guide](references/non-subscriber-mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, curl examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include environment variables, API request examples, and operational checklists for essesseff workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
