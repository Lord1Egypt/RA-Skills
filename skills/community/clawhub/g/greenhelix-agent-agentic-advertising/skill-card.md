## Description: <br>
Build autonomous ad-buying agents with publisher discovery, trust verification, escrow-based ad spend, real-time ROAS tracking, compliance guardrails, fleet-scale campaign management, and Python API examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media technologists, and advertising operations teams use this guide to design autonomous media-buying agents that can discover publishers, manage escrow-backed campaign budgets, track ROAS, and enforce approval and compliance guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable wallet, escrow, release, cancellation, and budget-allocation examples may move real ad spend if pointed at production accounts. <br>
Mitigation: Use sandbox or test accounts first, confirm endpoints before execution, enforce hard spending caps, and require explicit human approval before production campaign spend. <br>
Risk: The guide references both sandbox onboarding and production API usage, which can make the execution environment ambiguous. <br>
Mitigation: Label sandbox and production configurations separately and verify account, endpoint, and budget state before adapting any example. <br>
Risk: The skill requires an agent signing key, which is sensitive credential material. <br>
Mitigation: Store signing keys in a secret manager or environment-only configuration, rotate exposed keys, and avoid committing credentials into prompts, logs, or source files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-agentic-advertising) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>
- [GreenHelix production hardening companion skill](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-running educational content; examples require user-supplied credentials and environment configuration before adaptation.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
