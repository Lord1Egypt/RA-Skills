## Description: <br>
Source-distributed deterministic execution service with pinned dependencies that runs with signed approval artifacts in ClawShield mode, emits verifiable receipts, performs no outbound HTTP or governance calls, and avoids runtime package installation or dynamic downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendinghot](https://clawhub.ai/user/trendinghot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use OpenExec to route high-impact agent actions through a deterministic execution boundary with replay protection, signed approval checks in ClawShield mode, and verifiable receipts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Demo mode auto-approves registered actions. <br>
Mitigation: For production use, set OPENEXEC_MODE=clawshield and configure a trusted CLAWSHIELD_PUBLIC_KEY. <br>
Risk: Registered handlers execute with the hosting process privileges and OpenExec does not provide OS-level sandboxing. <br>
Mitigation: Run in a hardened container or VM, avoid running as root, audit handlers, and configure OPENEXEC_ALLOWED_ACTIONS. <br>
Risk: Network exposure or remote database configuration can expand the deployment trust boundary. <br>
Mitigation: Bind locally or place the service behind a firewall or reverse proxy, use TLS when externally reachable, and keep the database local or otherwise trusted. <br>
Risk: Stored payloads and results may contain sensitive audit data. <br>
Mitigation: Apply appropriate database access controls, retention policies, backups, and monitoring. <br>


## Reference(s): <br>
- [OpenExec ClawHub release](https://clawhub.ai/trendinghot/openexec-skill) <br>
- [ClawShield governance service](https://clawshield.forgerun.ai/) <br>
- [README](README.md) <br>
- [Security model](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with shell commands, configuration examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution responses include deterministic results and receipt hashes; receipt verification accepts JSON inputs.] <br>

## Skill Version(s): <br>
0.1.10 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
