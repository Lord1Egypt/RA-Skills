## Description:

Comprehensive guide and toolkit for publishing Java artifacts to Maven Central using the modern Central Portal (central.sonatype.com) workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misakiga](https://clawhub.ai/user/misakiga)

### License/Terms of Use:


## Use Case:

Developers and release engineers use this skill to configure Maven, GPG signing, and Central Portal publishing for Java or Kotlin libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Central Portal tokens or GPG passphrases may be stored in plaintext Maven settings or templates.

Mitigation: Use Maven credential encryption, CI secret injection, restrictive file permissions, and a protected signing setup; never commit real tokens or passphrases.

Risk: Publishing steps can release artifacts to Maven Central before credentials, signatures, or metadata are ready.

Mitigation: Review generated Maven settings and POM configuration, keep autoPublish disabled for first releases, and manually verify Central Portal deployments before publishing.

## Reference(s):

- [Central Portal](https://central.sonatype.com/)
- [Maven Central Publishing Requirements](https://central.sonatype.org/publish/requirements/)
- [Central Portal Deployments](https://central.sonatype.com/publishing/deployments)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and XML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Maven and GPG setup guidance, Maven plugin configuration, settings.xml examples, deployment commands, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
