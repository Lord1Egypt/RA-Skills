## Description:

Helps iOS developers and AI coding agents plan and execute CocoaPods to Swift Package Manager migrations by auditing dependencies, mapping SPM equivalents, translating build settings, handling resource and interop issues, and adapting CI/CD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changjiashuai](https://clawhub.ai/user/changjiashuai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate and carry out migrations from CocoaPods to Swift Package Manager in iOS projects, including enterprise dependency planning, build setting translation, verification, and CI/CD adaptation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated migration guidance may remove or alter CocoaPods build settings and CI steps in ways that break project builds.

Mitigation: Review generated project and CI changes before committing them, then run dependency resolution and full Xcode builds to verify imports, linking, resources, and Objective-C interop.

Risk: Skipping dependency audit can lead to incorrect SPM mappings, missing binary framework handling, or retained CocoaPods-only behavior.

Mitigation: Inventory every pod, subspec, version constraint, script phase, resource bundle, xcconfig include, module map, and bridging requirement before writing or applying Package.swift changes.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/changjiashuai/ios-migration-expert)
- [ClawHub skill page](https://clawhub.ai/changjiashuai/skills/ios-migration-expert)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include migration checklists, Package.swift guidance, Xcode build setting changes, and CI command updates.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
