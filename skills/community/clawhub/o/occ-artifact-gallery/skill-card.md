## Description:

Use when an agent generates local files/folders and must return mobile-accessible OCC/Tailscale viewer links instead of filesystem paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadoprizm](https://clawhub.ai/user/shadoprizm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to register generated files or folders and return mobile-accessible OCC/Tailscale viewer links instead of local filesystem paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled local executable and broken manifest references.

Mitigation: Verify artifact_gallery_tool.py, its ownership, permissions, manifest paths, and access controls in the intended OCC environment before installation.

Risk: Generated artifact links may expose sensitive files if gallery controls are not correctly configured.

Mitigation: Use the skill only after confirming the gallery root allowlist, secret-path rejection, authentication, and link visibility controls.

Risk: If artifact registration fails, invented URLs could mislead users or bypass intended path checks.

Mitigation: Report the registration failure or fix the path/root configuration instead of fabricating viewer or download URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shadoprizm/skills/occ-artifact-gallery)
- [Publisher profile](https://clawhub.ai/user/shadoprizm)
- [Gallery UI](https://n2-pro.tail1c2e65.ts.net/artifacts)
- [Artifact viewer URL pattern](https://n2-pro.tail1c2e65.ts.net/artifacts/a/{artifact_id})

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with inline shell commands and artifact viewer URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses should include a brief summary, viewer_url, optional download_url, and artifact type or size.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
