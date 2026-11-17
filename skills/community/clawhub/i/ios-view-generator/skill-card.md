## Description:

Generates Objective-C iOS view and view-controller code from screenshots, using lazy loading and separated UI, layout, and data-binding methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[near2sea](https://clawhub.ai/user/near2sea)

### License/Terms of Use:


## Use Case:

Developers use this skill to turn iOS UI screenshots into Objective-C UIViewController or view code with lazy-loaded components, estimated sizing and spacing, and separated setup, constraint, and data-binding methods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Objective-C UI code can contain inaccurate layout estimates, placeholder image names, or dependency snippets that do not match the target app.

Mitigation: Review and test generated code before using it in an app, with particular attention to sizing, spacing, image assets, and Masonry or native Auto Layout integration.

## Reference(s):

- [Objective-C view patterns](artifact/references/objc-view-patterns.md)
- [ClawHub skill page](https://clawhub.ai/near2sea/skills/ios-view-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Objective-C code blocks and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated code may include Masonry constraints by default, native Auto Layout fallback guidance, estimated dimensions and spacing, system colors, and placeholder image names.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
