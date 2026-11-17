## Description:

Micro-frontend architecture design and implementation guide for designing app boundaries, choosing Module Federation/qiankun/single-spa/wujie, splitting monoliths into sub-apps, implementing style isolation, setting up inter-app communication, and deploying micro-frontends independently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldath](https://clawhub.ai/user/goldath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and implement micro-frontend architectures, compare framework options, set up application shells and sub-apps, isolate styles, define inter-app communication, and deploy sub-apps independently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication-token examples may encourage storing bearer tokens in localStorage or sessionStorage or passing raw tokens into sub-apps.

Mitigation: Avoid bearer tokens in browser storage, avoid raw token propagation to sub-apps, and require a production authentication design review before applying the examples.

Risk: Dynamic remote-code-loading examples can be unsafe if origins, manifests, versions, and remote entries are not trusted and protected.

Mitigation: Use trusted origins, immutable versions, protected manifests, CSP, and integrity checks for remotely loaded micro-frontends.

Risk: Architecture guidance may be incomplete for a specific production environment.

Mitigation: Review the skill output before relying on it for production architecture decisions.

## Reference(s):

- [Module Federation](references/module-federation.md)
- [qiankun](references/qiankun.md)
- [single-spa](references/single-spa.md)
- [Inter-App Communication](references/communication.md)
- [Style Isolation](references/style-isolation.md)
- [Deployment](references/deployment.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, configuration, and comparison table examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Architecture guidance should be reviewed before production use, especially examples involving authentication tokens and remote code loading.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
