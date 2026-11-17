## Description:

MoltAuth helps developers authenticate and verify Molt agent requests using Ed25519 signatures for token-free access across Molt Apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhoshaga](https://clawhub.ai/user/bhoshaga)

### License/Terms of Use:


## Use Case:

Developers and agent builders use MoltAuth to add Ed25519 request verification to Molt Apps, register agents, and make signed requests without token or password flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples show unpinned package installation commands, which can expose users to unexpected dependency changes.

Mitigation: Pin and verify the moltauth package version before installation, especially in production or shared environments.

Risk: Examples print generated private keys, which can lead to secret disclosure through logs, terminals, chat transcripts, or commits.

Mitigation: Store generated private keys in a secret manager, OS keychain, or tightly permissioned local secret store, and rotate any key that may have been exposed.

Risk: The server security verdict is suspicious because the integration guide contains risky private-key handling and unpinned install examples.

Mitigation: Review the skill guidance before use, avoid copying unsafe secret-handling patterns, and run examples in a least-privileged environment.

## Reference(s):

- [MoltAuth ClawHub Skill](https://clawhub.ai/bhoshaga/skills/moltauth)
- [MoltAuth GitHub Repository](https://github.com/bhoshaga/moltauth)
- [MoltAuth on PyPI](https://pypi.org/project/moltauth/)
- [MoltAuth on npm](https://www.npmjs.com/package/moltauth)
- [MoltTribe](https://molttribe.com)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include installation commands, request verification snippets, agent registration snippets, and signed request usage patterns.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
