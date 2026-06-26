## Description: <br>
Upgrade Next.js to the latest version following official migration guides and codemods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TuanViDev](https://clawhub.ai/user/TuanViDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute Next.js upgrades by checking current dependencies, consulting official migration guides, running codemods, updating packages, and validating the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codemods and dependency updates can modify source files, configuration, and lockfiles in ways that introduce regressions. <br>
Mitigation: Run the skill on a branch or clean working tree, review all diffs, and run the project build and tests before merging or deploying. <br>
Risk: Using latest package versions can reduce reproducibility across environments. <br>
Mitigation: Pin target versions when reproducibility matters and confirm the selected upgrade path before applying package changes. <br>


## Reference(s): <br>
- [Next.js Codemods Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/codemods) <br>
- [Next.js Version 16 Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-16) <br>
- [Next.js Version 15 Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-15) <br>
- [Next.js Version 14 Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-14) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and code-change guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose codemod, dependency, TypeScript type, and configuration changes for review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
