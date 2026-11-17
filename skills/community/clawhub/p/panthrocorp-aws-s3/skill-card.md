## Description:

Self-contained AWS S3 SDK bundle for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panthrocorp](https://clawhub.ai/user/panthrocorp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent authors use this skill to package AWS S3 SDK access for gateway containers, enabling agents to call S3 commands without installing dependencies at runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned or unverified remote package could introduce the wrong release into the gateway container.

Mitigation: Install only from a pinned, verified tarball for the intended version.

Risk: Broad AWS credentials could allow agents to access S3 buckets or actions outside the intended use case.

Mitigation: Run with least-privilege AWS credentials limited to the required S3 buckets and actions.

Risk: Bundled dependencies can become stale if the package is rebuilt without review.

Mitigation: Review dependency updates before rebuilding the bundle.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panthrocorp/skills/panthrocorp-aws-s3)
- [Project homepage](https://github.com/PanthroCorp-Limited/openclaw-skills)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundles @aws-sdk/client-s3 and transitive dependencies for Node.js gateway containers.]

## Skill Version(s):

0.2.1 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
