## Description:

Openclaw Deploy helps agents package OpenClaw environments and provide shell-based guidance for local, remote, or batch deployment with conflict handling, logging, and integrity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyx058019](https://clawhub.ai/user/lyx058019)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to package OpenClaw configuration, workspace, skill, and Docker assets for migration, backup, or standardized deployment across local and SSH-managed hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can package local OpenClaw data, workspace files, and custom skills.

Mitigation: Package only intended content, avoid including workspace memory or custom skills unless sharing is deliberate, and inspect archives before deployment.

Risk: Deployment workflows can make changes on local or remote hosts.

Mitigation: Prefer backup or update modes over cover mode, verify host keys independently, and verify deployment packages before running them.

Risk: Included tests and deployment scripts may modify installed tools or target directories when run with broad privileges.

Mitigation: Run tests on disposable systems and avoid elevated privileges unless the target paths and effects have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyx058019/skills/lyx-openclaw-deploy)
- [OpenClaw Deploy install repository](https://github.com/lyx058019/openclaw-deploy)
- [Artifact README](artifact/docs/README.md)
- [Troubleshooting guide](artifact/docs/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline bash and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, tar, and ssh for the documented deployment workflows.]

## Skill Version(s):

1.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
