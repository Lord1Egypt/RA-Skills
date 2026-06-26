## Description: <br>
Audits JavaScript bundle artifacts from webpack, Vite, Rollup, and Next.js to identify large chunks, duplicate dependencies, treeshaking issues, budget violations, and CI enforcement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local JavaScript build output, understand bundle-size regressions, and prepare optimization or CI budget recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested package installs, removals, or CI workflow edits may change application behavior or build policy. <br>
Mitigation: Review proposed dependency and workflow changes, run the project test suite, and apply only changes that match the intended bundle-size policy. <br>
Risk: Auditing unrelated build output directories may expose or mix private project artifacts in the report. <br>
Mitigation: Run the skill only in the project intended for inspection and limit inputs to relevant local build artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-bundle-size-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include gzip size estimates, bundle budget findings, optimization suggestions, and CI fail-gate snippets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
