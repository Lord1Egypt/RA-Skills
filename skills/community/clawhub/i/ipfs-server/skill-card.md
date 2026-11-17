## Description:

Full IPFS node operations - install, configure, pin content, publish IPNS, manage peers, and run gateway services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apexfork](https://clawhub.ai/user/apexfork)

### License/Terms of Use:


## Use Case:

Developers, operators, and server administrators use this skill to install and operate an IPFS node, manage pinned content, publish IPNS records, configure networking, and run gateway services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Root-level installer guidance can execute unverified downloaded code with elevated privileges.

Mitigation: Prefer a trusted package manager, or verify Kubo checksums and signatures before using sudo with a downloaded installer.

Risk: Exposing the IPFS API or gateway can increase unauthorized access, abuse, or bandwidth consumption risk.

Mitigation: Keep the API bound to localhost unless firewalling and authentication are in place, and deliberately review public gateway exposure before deployment.

Risk: Remote pinning examples use JWT-style credentials that could be exposed through shell history or shared terminals.

Mitigation: Handle remote-pinning tokens outside shared command history and avoid entering real secrets directly into reusable shell sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apexfork/skills/ipfs-server)
- [Publisher Profile](https://clawhub.ai/user/apexfork)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the IPFS CLI (Kubo) and sufficient local storage and bandwidth for node operation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
