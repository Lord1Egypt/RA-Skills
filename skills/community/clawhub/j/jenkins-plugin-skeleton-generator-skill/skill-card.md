## Description:

Generate a Jenkins plugin skeleton based on the Jenkins version and JDK version provided by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoyim](https://clawhub.ai/user/leoyim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to collect Jenkins, JDK, Maven, and plugin metadata, validate compatibility, and generate a Jenkins plugin project skeleton with Maven configuration, Java extension classes, Jelly UI resources, README content, and build/install guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Jenkins plugin code may include credential, token, password, persistent configuration, listener, or periodic-task behavior that affects a Jenkins instance.

Mitigation: Review those areas before production use, replace secret-bearing String fields with Jenkins Secret-backed handling, and confirm behavior before uploading the plugin to Jenkins.

Risk: A Jenkins, JDK, Maven, parent POM, or extension-point mismatch can lead to build, installation, or runtime failures.

Mitigation: Use the skill's compatibility checks and troubleshooting references to verify Jenkins/JDK compatibility, selected parent POM, repository configuration, and generated extension behavior before packaging the HPI.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leoyim/skills/jenkins-plugin-skeleton-generator-skill)
- [Jenkins Plugin Development Documentation](https://www.jenkins.io/doc/developer/)
- [Jenkins Java Support Policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/index.html)
- [Jenkins Plugin Parent POM](https://github.com/jenkinsci/plugin-pom)
- [Jenkins Hello World Plugin](https://github.com/jenkinsci/hello-world-plugin/)
- [Jenkins Repository Proxy](https://repo.jenkins-ci.org/public/)
- [Compatibility Check](artifact/references/compatibility-check.md)
- [Plugin Types / Extension Points](artifact/references/plugin-types.md)
- [Trigger Timing Reference](artifact/references/trigger-timing-reference.md)
- [Jelly Form Controls Reference](artifact/references/jelly-reference.md)
- [Troubleshooting Guide](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with generated file contents and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a multi-file Jenkins HPI plugin skeleton, including pom.xml, Java sources, Jelly resources, README content, and build/install steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
