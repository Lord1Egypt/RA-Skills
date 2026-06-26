# Security Policy

## Supported versions

Only the latest published version of the `moltbank` skill and the `@moltbankhq/cli` package receives security updates. Older versions are not patched.

| Component | Supported |
| --- | --- |
| `moltbank` skill (latest release) | Yes |
| `@moltbankhq/cli` (latest published) | Yes |
| Any older release | No |

## Reporting a vulnerability

Please report suspected vulnerabilities privately. Do **not** file a public GitHub issue for security reports.

- Email: `security@moltbank.bot`
- Or open a private GitHub security advisory on this repository.

Please include:

- affected component (skill, CLI, or both) and version
- reproduction steps or proof-of-concept
- impact assessment (confidentiality, integrity, availability, financial)
- whether the issue has been disclosed elsewhere

We aim to acknowledge reports within 3 business days and to provide an initial assessment within 7 business days.

## In scope

- Remote code execution, command injection, or arbitrary install paths triggered through the skill's update or setup flows
- Prompt-injection paths that cause the agent to execute unapproved install/update commands, bypass domain validation, or move funds without explicit user approval
- Authentication bypass, token exfiltration, or credential leakage from the local `moltbank` CLI
- x402 or payment flows that can execute without explicit user approval
- Provenance or supply-chain issues affecting `@moltbankhq/cli` releases

## Out of scope

- Findings that require the user to knowingly run commands not listed in `SKILL.md` under "Approved update commands"
- Findings against third-party agents, runtimes, or skill managers themselves (report those to the respective maintainers)
- Issues in preview/dev branches that are not published to end users
- Theoretical issues without a demonstrated impact

## Coordinated disclosure

We prefer coordinated disclosure. Once a fix is available and released, we will publish an advisory crediting the reporter (unless anonymity is requested).
