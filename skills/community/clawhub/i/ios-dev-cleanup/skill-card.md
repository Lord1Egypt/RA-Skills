## Description:

Use when checking iOS development disk usage or cleaning up simulators, runtimes, device support, derived data, CocoaPods cache, archives, or other build artifacts; scans each category, shows top 5 by size with last-used info, and offers safe deletion commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesseluo](https://clawhub.ai/user/jesseluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local macOS/Xcode disk usage across simulator runtimes, simulator devices, DerivedData, CocoaPods, DeviceSupport, archives, Swift Package Manager caches, and Xcode caches. It helps them review proposed cleanup actions and run deletion commands after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently delete local iOS and Xcode development artifacts, including archives that may contain important release builds.

Mitigation: Require explicit user approval before each deletion and review archive deletion separately before executing cleanup commands.

Risk: The artifact describes automatic cleanup of unavailable simulators and runtimes before the full review workflow.

Mitigation: Require approval for unavailable simulator and runtime deletion as directed by the security guidance, even when the items appear unusable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jesseluo/skills/ios-dev-cleanup)
- [Artifact README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports disk usage summaries, top items by size, proposed cleanup commands, and before/after cleanup results.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
