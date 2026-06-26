## Description: <br>
Post and reply to X/Twitter and Farcaster with text and images, including multi-account support, dynamic Twitter tier detection, content variation, draft preview, character validation, threads, replies, image uploads, consumption-based X API pricing, and pay-per-cast Farcaster posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teeclaw](https://clawhub.ai/user/teeclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and social operators use this skill to draft, validate, post, and reply across X/Twitter and Farcaster from command-line workflows. It is intended for managed social publishing where credentials, account costs, and platform side effects are reviewed before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post or reply through live X/Twitter and Farcaster accounts. <br>
Mitigation: Install only for accounts where posting authority is acceptable, test with isolated accounts, and review draft previews before confirming live actions. <br>
Risk: Credentials and private keys are required for X/Twitter and Farcaster workflows. <br>
Mitigation: Store credentials securely, restrict file permissions, avoid sharing private keys, and avoid using sensitive images or private URLs. <br>
Risk: Security evidence flags anti-spam evasion behavior and live-account side effects as suspicious. <br>
Mitigation: Review the content variation behavior and platform policy implications before enabling automated or repeated posting. <br>
Risk: Security guidance warns not to rely on --dry-run for Twitter tier detection until live POST behavior is fixed. <br>
Mitigation: Treat Twitter tier detection as potentially live-impacting and test only with accounts prepared for possible API side effects. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teeclaw/openclaw-social-post) <br>
- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard) <br>
- [X API Pricing](https://developer.twitter.com/#pricing) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces social post or reply actions when scripts are executed; dry-run and preview modes can show proposed content before posting.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
