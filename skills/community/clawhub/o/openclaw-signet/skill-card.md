## Description:

Openclaw Signet signs installed agent skills with SHA-256 content hashes and verifies whether their files were modified, added, or removed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to establish a local trust manifest for installed agent skills, then check whether those skill directories still match their signed state. It supports routine verification and investigation of changed skill files in OpenClaw-compatible workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports that file mutation and snapshot logic can delete or copy data outside the intended skill directory.

Mitigation: Run mutation-capable commands only in trusted, backed-up workspaces, and avoid restore, protect, reject, snapshot, or quarantine on untrusted input until validation, symlink handling, and overwrite/delete safeguards are fixed.

Risk: The security verdict is suspicious for this release.

Mitigation: Review and scan the skill before deployment, and use the signing and verification commands separately from mutation-capable recovery commands when only tamper detection is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atlaspa/skills/openclaw-signet)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain-text CLI reports plus JSON manifest, snapshot, and evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and runs locally without external dependencies.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
