## Description:

Bridge macOS-only tools into a Linux OpenClaw gateway via SSH wrappers and connected Mac nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to expose Mac-only command-line tools to a Linux OpenClaw gateway through explicit SSH wrappers, verification steps, and publishable wrapper contracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted host or path values could run unintended commands through generated SSH wrappers.

Mitigation: Install only with trusted host, path, key, and known-hosts values; validate SSH destinations and safely serialize wrapper configuration before wider use.

Risk: The bridge grants a Linux gateway remote access to Mac-side tools and data surfaces.

Mitigation: Use dedicated SSH keys, non-root Mac accounts, known-hosts pinning where feasible, and one wrapper per tool instead of a broad shell bridge.

Risk: A missing or unavailable Mac node can disrupt workflows that depend on Mac-only tools.

Mitigation: Verify each remote binary before publishing, document node ownership, and fail with a clear degraded state while keeping unrelated gateway tools running.

Risk: Existing wrapper files may be overwritten during installation.

Mitigation: Review target wrapper names and install directories before running installers, and keep rollback steps for removing individual wrappers.

## Reference(s):

- [Security Model](references/security-model.md)
- [Publish Pattern](references/publish-pattern.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wrapper installation and verification steps for SSH access to Mac-side tools.]

## Skill Version(s):

0.6.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
