## Description:

Upgrade Next.js to the latest version following official migration guides and codemods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanvidev](https://clawhub.ai/user/tuanvidev)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and perform Next.js upgrades by detecting dependency versions, consulting official upgrade guides, running codemods, updating packages, and verifying the application build.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Codemods and dependency upgrades may change source code and package versions.

Mitigation: Run the skill on a clean branch, review the exact npm package versions and codemod command before execution, and inspect all generated diffs before accepting them.

Risk: Next.js major-version migrations can introduce build or runtime regressions that require manual follow-up.

Mitigation: Run the project build, start the development server, and test key functionality after applying the upgrade.

## Reference(s):

- [Next.js Upgrade Codemods](https://nextjs.org/docs/app/guides/upgrading/codemods)
- [Next.js Version 16 Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-16)
- [Next.js Version 15 Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-15)
- [Next.js Version 14 Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-14)
- [ClawHub Skill Page](https://clawhub.ai/tuanvidev/skills/next-upgrade)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update dependency manifests and source files when executed in a project.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
