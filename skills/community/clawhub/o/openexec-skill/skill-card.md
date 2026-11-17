## Description:

OpenExec is a source-distributed deterministic execution service with pinned dependencies, signed approval enforcement in ClawShield mode, verifiable receipts, no outbound governance calls, and no runtime package installation or dynamic downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendinghot](https://clawhub.ai/user/trendinghot)

### License/Terms of Use:


## Use Case:

Developers and engineers use OpenExec to route approved AI-system actions through a deterministic execution boundary with replay protection, signed approval checks in ClawShield mode, and verifiable receipts. It is intended for architectures that separate proposal, authorization, execution, and witnessing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence says approval, replay, and receipt guarantees are weaker than documented for production or high-impact use.

Mitigation: Use only for local demo or isolated evaluation until approvals are single-use, replay retrieval is authorization-bound, receipts are signed or HMAC-protected, dependencies are reviewed, ClawShield mode is enforced, and an explicit action allow-list is configured.

Risk: Registered handlers execute with the privileges of the hosting process and the skill does not provide OS-level sandboxing.

Mitigation: Run inside a hardened container or VM, avoid root execution, restrict allowed actions, and audit registered handlers before use.

Risk: Inbound HTTP endpoints can receive execution and receipt-verification requests.

Mitigation: Bind to localhost by default, place externally reachable deployments behind firewall or reverse proxy controls, and use TLS outside localhost.

## Reference(s):

- [OpenExec Skill Page](https://clawhub.ai/trendinghot/skills/openexec-skill)
- [Publisher Profile](https://clawhub.ai/user/trendinghot)
- [README](artifact/README.md)
- [Security Model](artifact/SECURITY.md)
- [ClawShield Governance Layer](https://clawshield.forgerun.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP endpoint examples, environment variable settings, configuration guidance, and operational hardening notes.]

## Skill Version(s):

0.1.10 (source: frontmatter, release evidence, main.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
