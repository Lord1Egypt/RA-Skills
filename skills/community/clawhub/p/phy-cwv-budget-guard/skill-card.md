## Description: <br>
Core Web Vitals budget enforcer that runs Lighthouse against a local dev server or staging URL, extracts LCP, INP, CLS, FCP, and TTFB scores, compares against a project .cwv-budget.json config, and fails CI if any metric regresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to audit local or staging web pages for Core Web Vitals regressions, compare results against project budgets, and receive concrete remediation guidance before changes ship. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local npm, npx, Lighthouse, Chrome, and Python commands against URLs supplied by the user. <br>
Mitigation: Use explicit /cwv-check invocations with trusted local or staging URLs, and review generated commands before running them in sensitive environments. <br>
Risk: Generated reports and history can contain staging URLs, branch names, git SHAs, and performance details. <br>
Mitigation: Avoid auditing sensitive authenticated pages unless intended, and add cwv-report.json and .cwv-history.json to .gitignore when those files should remain local. <br>
Risk: First-run npx or npm usage may download local tooling before Lighthouse runs. <br>
Mitigation: Prefer pinned project dev dependencies such as @lhci/cli in controlled CI environments. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-cwv-budget-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with metric tables, inline shell commands, JSON configuration examples, and code remediation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local audit artifacts such as cwv-report.json, .cwv-budget.json, and .cwv-history.json in the audited project.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
