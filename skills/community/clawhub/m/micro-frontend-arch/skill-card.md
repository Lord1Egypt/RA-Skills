## Description: <br>
Micro-frontend architecture design and implementation guide for choosing framework patterns, splitting monoliths, isolating styles, coordinating inter-app communication, and deploying sub-apps independently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goldath](https://clawhub.ai/user/goldath) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement micro-frontend architectures across Module Federation, qiankun, single-spa, communication, style isolation, and independent deployment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication-token examples use localStorage or pass tokens into sub-app props, which can be unsafe if copied directly into production. <br>
Mitigation: Replace these examples with HttpOnly SameSite cookies, backend-managed sessions, or tightly scoped in-memory tokens, and avoid passing raw tokens to sub-apps. <br>
Risk: Remote-loading and deployment-manifest workflows can introduce supply-chain or rollback risk if origins and deployment controls are weak. <br>
Mitigation: Use trusted origins, CI approvals, least-privilege credentials, and rollback controls for remote entries and deployment manifests. <br>


## Reference(s): <br>
- [Module Federation](references/module-federation.md) <br>
- [qiankun](references/qiankun.md) <br>
- [single-spa](references/single-spa.md) <br>
- [Inter-App Communication](references/communication.md) <br>
- [Style Isolation](references/style-isolation.md) <br>
- [Deployment](references/deployment.md) <br>
- [ClawHub skill page](https://clawhub.ai/goldath/micro-frontend-arch) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript, JSX, YAML, JSON, CSS, HTML, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance with implementation snippets and comparison tables.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
