## Description: <br>
Comprehensive guide and toolkit for publishing Java artifacts to Maven Central using the modern Central Portal (central.sonatype.com) workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MISAKIGA](https://clawhub.ai/user/MISAKIGA) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to configure Maven projects, GPG signing, Central Portal credentials, and deployment steps for publishing Java or Kotlin libraries to Maven Central. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maven Central tokens and GPG passphrases may be stored persistently in Maven settings. <br>
Mitigation: Protect ~/.m2/settings.xml with restrictive permissions, never commit it, and prefer encrypted Maven passwords, environment variables, CI secrets, or a keychain. <br>
Risk: The included Aliyun Maven mirror changes dependency source behavior. <br>
Mitigation: Remove the mirror unless the user intentionally trusts and needs it for their environment. <br>
Risk: Publishing configuration can release artifacts to Maven Central if credentials and deployment commands are used. <br>
Mitigation: Review generated configuration and keep autoPublish disabled until the deployment is manually inspected in Central Portal. <br>


## Reference(s): <br>
- [Central Portal](https://central.sonatype.com/) <br>
- [Maven Central Publishing Requirements](https://central.sonatype.org/publish/requirements/) <br>
- [Central Portal Deployments](https://central.sonatype.com/publishing/deployments) <br>
- [ClawHub Skill Page](https://clawhub.ai/MISAKIGA/maven-central-publish) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with XML configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Maven and GPG setup steps, publishing configuration, deployment commands, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
