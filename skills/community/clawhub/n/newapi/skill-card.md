## Description:

Assistant for newapi (new-api), an open-source unified AI gateway platform (https://github.com/QuantumNous/new-api). Use when the user asks about New API, managing models, groups, balance, or tokens, or securely copying keys, applying them to config files, or using them in commands without exposing secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calcium-ion](https://clawhub.ai/user/calcium-ion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who administer New API instances use this skill to list models, groups, account balance, and token metadata; create and update tokens; and apply token keys to local tooling without displaying secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles New API management credentials, API token keys, local clipboard access, and config files selected by the user.

Mitigation: Install only when that access is acceptable, prefer narrowly scoped config files, keep New API credentials out of broad project .env files, and avoid using the skill on shared machines.

Risk: The exec-token action can run shell commands with a retrieved token substituted into the command.

Mitigation: Use exec-token only for trusted commands that the user explicitly requested, and prefer apply-token when a target application can read credentials from a config file.

Risk: Secret redaction for scanned config files and command output is best effort and may miss uncommon formats.

Mitigation: Treat sanitized output as risk reduction rather than proof that no secret remains, and avoid asking the assistant to inspect files likely to contain unrelated credentials.

Risk: The release source is unpinned and server evidence does not provide GitHub import provenance for this version.

Mitigation: Review the ClawHub release evidence and source artifact before installing or updating the skill.

## Reference(s):

- [New API GitHub Repository](https://github.com/QuantumNous/new-api)
- [New API Website](https://www.newapi.ai)
- [New API API Reference Index](https://apifox.newapi.ai/llms.txt)
- [New API Product Docs Index](https://www.newapi.ai/llms.txt)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with tables and inline shell commands; helper actions may return sanitized JSON or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May copy token keys to the local clipboard or update user-selected configuration files when those actions are explicitly invoked.]

## Skill Version(s):

0.1.1 (source: server release metadata and user changelog, released 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
