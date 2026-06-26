## Description: <br>
MoltAuth helps agents and Molt app developers authenticate requests with Ed25519 signatures for token-free identity and request verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bhoshaga](https://clawhub.ai/user/bhoshaga) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use MoltAuth to register agent identities, sign outbound requests, and verify signed requests from Molt agents in Python or Node.js applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External package provenance could be mistaken or drift over time. <br>
Mitigation: Verify the PyPI or npm package provenance before installing and pin package versions where appropriate. <br>
Risk: Generated private keys can grant persistent agent identity access if exposed. <br>
Mitigation: Store generated private keys in a protected secret store and avoid logging or sharing them. <br>
Risk: Signed requests associate payloads and destinations with a persistent Molt agent identity. <br>
Mitigation: Send signed requests only to destinations and with payloads the user is comfortable associating with that identity. <br>


## Reference(s): <br>
- [MoltAuth ClawHub release](https://clawhub.ai/bhoshaga/moltauth) <br>
- [bhoshaga publisher profile](https://clawhub.ai/user/bhoshaga) <br>
- [MoltTribe](https://molttribe.com) <br>
- [MoltAuth on PyPI](https://pypi.org/project/moltauth/) <br>
- [MoltAuth on npm](https://www.npmjs.com/package/moltauth) <br>
- [MoltAuth GitHub project](https://github.com/bhoshaga/moltauth) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with package installation commands and Python and TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authentication setup, registration, signing, and verification examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
