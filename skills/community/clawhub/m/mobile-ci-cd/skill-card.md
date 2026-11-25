## Description:

Writes and hardens CI/CD pipelines for Android, iOS and Flutter on GitHub Actions and GitLab CI: Gradle and xcodebuild builds, lint and tests, signing from secrets, fastlane, Play and TestFlight upload, Firebase App Distribution, caching and SHA-pinned actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile engineers use this skill to create, fix, speed up, and review CI/CD pipelines for Android, iOS, Flutter, and Kotlin Multiplatform projects, including build verification, signing, and app distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some CI examples use elevated privileges, which can increase the impact of a compromised or misconfigured job.

Mitigation: Review privileged commands and restrict them to the required job and runner permissions.

Risk: Firebase CLI examples use an unpinned version, so a later release could change what a pipeline installs.

Mitigation: Choose and pin a reviewed Firebase CLI version before using the example in a release workflow.

Risk: The security review had limited coverage, including partial inspection of an Android reference.

Mitigation: Review the Android workflow and its commands before adopting them in a project pipeline.

## Reference(s):

- [Android on GitHub Actions](references/android-github-actions.md)
- [iOS on GitHub Actions](references/ios-github-actions.md)
- [Flutter on GitHub Actions](references/flutter-github-actions.md)
- [GitLab CI](references/gitlab-ci.md)
- [Mobile CI/CD on ClawHub](https://clawhub.ai/ahmadhussain0335/skills/mobile-ci-cd)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown guidance with YAML, Ruby, Gradle, and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pipeline files, required-secret lists, and manual setup steps.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
