## Description: <br>
Secure API key management for OpenClaw that stores, lists, tests, and deletes API keys without exposing them in chat history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christiancattaneo](https://clawhub.ai/user/christiancattaneo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use ipeaky to manage provider API keys for OpenClaw skills, including storing keys in OpenClaw config paths, listing masked keys, testing provider credentials, and deleting stored entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential-handling safety claims may be stronger than the reviewed behavior. <br>
Mitigation: Review the credential-handling limits before installation and prefer the v3 single-key storage path over v4 until v4 avoids visible input and argv/env exposure. <br>
Risk: Key tests send the supplied key to the selected provider API. <br>
Mitigation: Run provider key tests only when intentional, and use test or least-privileged keys where possible. <br>
Risk: Paid-tier Stripe scripts can store a Stripe secret and create checkout sessions. <br>
Mitigation: Do not run the Stripe scripts unless billing setup is intended; review and customize checkout settings before using live credentials. <br>
Risk: The secure input popup depends on macOS osascript. <br>
Mitigation: Use the macOS flow where osascript is available; on Linux or Windows, rely on stdin-based input paths documented by the skill. <br>


## Reference(s): <br>
- [ClawHub ipeaky release page](https://clawhub.ai/christiancattaneo/ipeaky) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [README](README.md) <br>
- [Paid tier README](paid_tier/README-paid.md) <br>
- [Stripe products dashboard](https://dashboard.stripe.com/products) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and OpenClaw config paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local shell scripts, OpenClaw config operations, and provider or Stripe API calls when the user chooses key testing or billing setup.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
